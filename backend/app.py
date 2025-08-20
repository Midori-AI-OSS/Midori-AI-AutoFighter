from __future__ import annotations

import json
import time
import copy
import random
import base64
import hashlib
import asyncio

from uuid import uuid4
from pathlib import Path
from dataclasses import asdict
from typing import Any
from typing import Awaitable
from typing import Callable

from quart import Quart
from quart import jsonify
from quart import request
from quart import send_from_directory

from cryptography.fernet import Fernet

from plugins import passives as passive_plugins
from plugins import players as player_plugins
from autofighter.cards import award_card
from autofighter.relics import award_relic
from autofighter.party import Party
from autofighter.rooms import BattleRoom
from autofighter.rooms import BossRoom
from autofighter.rooms import ChatRoom
from autofighter.rooms import RestRoom
from autofighter.rooms import ShopRoom
from autofighter.rooms import _choose_foe
from autofighter.rooms import _scale_stats
from autofighter.rooms import _serialize
from autofighter.stats import apply_status_hooks
from autofighter.gacha import GachaManager
from autofighter.mapgen import MapGenerator
from autofighter.mapgen import MapNode
from plugins.players._base import PlayerBase
from autofighter.save_manager import SaveManager


SAVE_MANAGER = SaveManager.from_env()
SAVE_MANAGER.migrate(Path(__file__).resolve().parent / "migrations")
with SAVE_MANAGER.connection() as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS damage_types (id TEXT PRIMARY KEY, type TEXT)"
    )
    count = conn.execute("SELECT COUNT(*) FROM owned_players").fetchone()[0]
    if count == 1:
        persona = random.choice(["lady_darkness", "lady_light"])
        conn.execute("INSERT INTO owned_players (id) VALUES (?)", (persona,))

FERNET_KEY = base64.urlsafe_b64encode(
    hashlib.sha256((SAVE_MANAGER.key or "plaintext").encode()).digest()
)
FERNET = Fernet(FERNET_KEY)

app = Quart(__name__)

battle_tasks: dict[str, asyncio.Task] = {}
battle_snapshots: dict[str, dict[str, Any]] = {}


@app.get("/")
async def status() -> tuple[str, int, dict[str, str]]:
    return jsonify({"status": "ok"})


@app.after_request
async def add_cors_headers(response):
    # Allow frontend dev server to call backend during development
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
    return response


# Expose static assets (e.g., backgrounds) for simple image serving
ASSETS_DIR = Path(__file__).resolve().parent / "assets"


@app.get("/assets/<path:filename>")
async def assets(filename: str):
    return await send_from_directory(ASSETS_DIR, filename)


def _passive_names(ids: list[str]) -> list[str]:
    names: list[str] = []
    for pid in ids:
        for mod in passive_plugins.__all__:
            cls = getattr(passive_plugins, mod)
            if getattr(cls, "id", None) == pid:
                names.append(getattr(cls, "name", pid))
                break
    return names


def _assign_damage_type(player: PlayerBase) -> None:
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT type FROM damage_types WHERE id = ?", (player.id,))
        row = cur.fetchone()
        if row:
            player.base_damage_type = row[0]
        else:
            conn.execute(
                "INSERT INTO damage_types (id, type) VALUES (?, ?)",
                (player.id, player.base_damage_type),
            )


def _load_player_customization() -> tuple[str, dict[str, int]]:
    pronouns = ""
    stats: dict[str, int] = {"hp": 0, "attack": 0, "defense": 0}
    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
        )
        cur = conn.execute(
            "SELECT value FROM options WHERE key = ?", ("player_pronouns",)
        )
        row = cur.fetchone()
        if row:
            pronouns = row[0]
        cur = conn.execute("SELECT value FROM options WHERE key = ?", ("player_stats",))
        row = cur.fetchone()
        if row:
            try:
                stats.update(json.loads(row[0]))
            except (TypeError, ValueError, json.JSONDecodeError):
                pass
    return pronouns, stats


def _apply_player_stats(
    player: PlayerBase,
    stats: dict[str, int] | None = None,
) -> None:
    _, loaded = _load_player_customization()
    if stats is None:
        stats = loaded
    hp_mod = 1 + stats.get("hp", 0) * 0.01
    atk_mod = 1 + stats.get("attack", 0) * 0.01
    def_mod = 1 + stats.get("defense", 0) * 0.01
    player.max_hp = player.hp = int(player.hp * hp_mod)
    player.atk = int(player.atk * atk_mod)
    player.defense = int(player.defense * def_mod)


@app.get("/gacha")
async def gacha_state() -> tuple[str, int, dict[str, object]]:
    manager = GachaManager(SAVE_MANAGER)
    return jsonify(manager.get_state())


@app.post("/gacha/pull")
async def gacha_pull() -> tuple[str, int, dict[str, object]]:
    data = await request.get_json(silent=True) or {}
    count = int(data.get("count", 1))
    manager = GachaManager(SAVE_MANAGER)
    try:
        results = manager.pull(count)
    except ValueError:
        return jsonify({"error": "invalid count"}), 400
    except PermissionError:
        return jsonify({"error": "insufficient tickets"}), 403
    state = manager.get_state()
    state["results"] = [asdict(r) for r in results]
    return jsonify(state)


@app.post("/gacha/auto-craft")
async def gacha_auto_craft() -> tuple[str, int, dict[str, object]]:
    data = await request.get_json(silent=True) or {}
    enabled = bool(data.get("enabled"))
    manager = GachaManager(SAVE_MANAGER)
    manager.set_auto_craft(enabled)
    return jsonify({"status": "ok", "auto_craft": enabled})


@app.post("/gacha/craft")
async def gacha_craft() -> tuple[str, int, dict[str, object]]:
    manager = GachaManager(SAVE_MANAGER)
    items = manager.craft()
    return jsonify({"status": "ok", "items": items})


@app.post("/run/start")
async def start_run() -> tuple[str, int, dict[str, object]]:
    data = await request.get_json(silent=True) or {}
    members: list[str] = data.get("party", [])
    damage_type = (data.get("damage_type") or "").capitalize()

    if (
        "player" not in members
        or not 1 <= len(members) <= 5
        or len(set(members)) != len(members)
    ):
        return jsonify({"error": "invalid party"}), 400

    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT id FROM owned_players")
        owned = {row[0] for row in cur.fetchall()}
    for mid in members:
        if mid != "player" and mid not in owned:
            return jsonify({"error": "unowned character"}), 400

    if damage_type:
        allowed = {"Light", "Dark", "Wind", "Lightning", "Fire", "Ice"}
        if damage_type not in allowed:
            return jsonify({"error": "invalid damage type"}), 400
        with SAVE_MANAGER.connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO damage_types (id, type) VALUES (?, ?)",
                ("player", damage_type),
            )

    run_id = str(uuid4())
    generator = MapGenerator(run_id)
    nodes = generator.generate_floor()
    state = {
        "rooms": [n.to_dict() for n in nodes],
        "current": 1,
        "battle": False,
        "awaiting_card": False,
        "awaiting_relic": False,
        "awaiting_next": False,
    }
    pronouns, stats = _load_player_customization()
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute(
            "SELECT type FROM damage_types WHERE id = ?",
            ("player",),
        )
        row = cur.fetchone()
    player_type = row[0] if row else player_plugins.player.Player().base_damage_type
    snapshot = {
        "pronouns": pronouns,
        "damage_type": player_type,
        "stats": stats,
    }
    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "INSERT INTO runs (id, party, map) VALUES (?, ?, ?)",
            (
                run_id,
                json.dumps(
                    {
                        "members": members,
                        "gold": 0,
                        "relics": [],
                        "cards": [],
                        "exp": {pid: 0 for pid in members},
                        "level": {pid: 1 for pid in members},
                        "player": snapshot,
                    }
                ),
                json.dumps(state),
            ),
        )

    party_info: list[dict[str, object]] = []
    for pid in members:
        for name in player_plugins.__all__:
            cls = getattr(player_plugins, name)
            if cls.id == pid:
                inst = cls()
                inst.exp = 0
                inst.level = 1
                _assign_damage_type(inst)
                party_info.append(
                    {
                        "id": inst.id,
                        "name": inst.name,
                        "passives": _passive_names(getattr(inst, "passives", [])),
                        "exp": inst.exp,
                        "level": inst.level,
                    }
                )
                break

    return jsonify({"run_id": run_id, "map": state, "party": party_info})


@app.put("/party/<run_id>")
async def update_party(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    members = data.get("party", [])
    gold = data.get("gold", 0)
    relics = data.get("relics", [])
    cards = data.get("cards", [])
    party = {
        "members": members,
        "gold": gold,
        "relics": relics,
        "cards": cards,
        "exp": {pid: 0 for pid in members},
        "level": {pid: 1 for pid in members},
    }
    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "UPDATE runs SET party = ? WHERE id = ?",
            (json.dumps(party), run_id),
        )
    return jsonify({"status": "ok"})


@app.get("/map/<run_id>")
async def get_map(run_id: str) -> tuple[str, int, dict[str, str]]:
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT map FROM runs WHERE id = ?", (run_id,))
        row = cur.fetchone()
    if row is None:
        return jsonify({"error": "run not found"}), 404
    return jsonify({"map": json.loads(row[0])})


@app.delete("/run/<run_id>")
async def end_run(run_id: str) -> tuple[str, int, dict[str, str]]:
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("DELETE FROM runs WHERE id = ?", (run_id,))
        if cur.rowcount == 0:
            return jsonify({"error": "run not found"}), 404
    return jsonify({"status": "ended"})


@app.post("/save/wipe")
async def wipe_save() -> tuple[str, int, dict[str, str]]:
    # Remove the entire save database and recreate it from migrations so a wipe
    # behaves like a fresh install. Future tables must be added to the
    # migrations directory; otherwise they will be lost here.
    SAVE_MANAGER.db_path.unlink(missing_ok=True)
    SAVE_MANAGER.migrate(Path(__file__).resolve().parent / "migrations")
    persona = random.choice(["lady_darkness", "lady_light"])
    with SAVE_MANAGER.connection() as conn:
        conn.execute("INSERT INTO owned_players (id) VALUES (?)", (persona,))
        conn.execute(
            "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS damage_types (id TEXT PRIMARY KEY, type TEXT)"
        )
    return jsonify({"status": "wiped"})


@app.get("/save/backup")
async def backup_save() -> tuple[bytes, int, dict[str, str]]:
    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS damage_types (id TEXT PRIMARY KEY, type TEXT)"
        )
        runs = conn.execute("SELECT id, party, map FROM runs").fetchall()
        options = conn.execute("SELECT key, value FROM options").fetchall()
        dmg = conn.execute("SELECT id, type FROM damage_types").fetchall()
    payload = {
        "runs": runs,
        "options": options,
        "damage_types": dmg,
    }
    data = json.dumps(payload)
    digest = hashlib.sha256(data.encode()).hexdigest()
    package = json.dumps({"hash": digest, "data": data}).encode()
    token = FERNET.encrypt(package)
    headers = {
        "Content-Type": "application/octet-stream",
        "Content-Disposition": "attachment; filename=backup.afsave",
    }
    return token, 200, headers


@app.post("/save/restore")
async def restore_save() -> tuple[str, int, dict[str, str]]:
    blob = await request.get_data()
    try:
        package = FERNET.decrypt(blob)
        obj = json.loads(package)
    except Exception:
        return jsonify({"error": "invalid backup"}), 400
    data = obj.get("data", "")
    digest = obj.get("hash", "")
    if hashlib.sha256(data.encode()).hexdigest() != digest:
        return jsonify({"error": "hash mismatch"}), 400
    payload = json.loads(data)
    with SAVE_MANAGER.connection() as conn:
        conn.execute("DELETE FROM runs")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
        )
        conn.execute("DELETE FROM options")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS damage_types (id TEXT PRIMARY KEY, type TEXT)"
        )
        conn.execute("DELETE FROM damage_types")
        conn.executemany(
            "INSERT INTO runs (id, party, map) VALUES (?, ?, ?)", payload["runs"]
        )
        conn.executemany(
            "INSERT INTO options (key, value) VALUES (?, ?)", payload["options"]
        )
        conn.executemany(
            "INSERT INTO damage_types (id, type) VALUES (?, ?)", payload["damage_types"]
        )
    return jsonify({"status": "restored"})


@app.get("/rooms/images")
async def room_images() -> tuple[str, int, dict[str, str]]:
    # Basic mapping of room types to background images
    mapping = {
        "battle-weak": "textures/backgrounds/background_01.png",
        "battle-normal": "textures/backgrounds/background_01.png",
        "battle-boss-floor": "textures/backgrounds/background_01.png",
        "shop": "textures/backgrounds/background_02.png",
        "rest": "textures/backgrounds/background_03.png",
    }
    images = {key: f"/assets/{rel}" for key, rel in mapping.items()}
    return jsonify({"images": images})


@app.get("/players")
async def get_players() -> tuple[str, int, dict[str, str]]:
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT id FROM owned_players")
        owned = {row[0] for row in cur.fetchall()}
    roster = []
    for name in player_plugins.__all__:
        cls = getattr(player_plugins, name)
        inst = cls()
        _assign_damage_type(inst)
        if inst.id == "player":
            _apply_player_stats(inst)
        stats = asdict(inst)
        stats["char_type"] = inst.char_type.name
        roster.append(
            {
                "id": inst.id,
                "name": inst.name,
                "owned": inst.id in owned,
                "is_player": inst.id == "player",
                "element": inst.base_damage_type,
                "stats": stats,
            }
        )
    return jsonify({"players": roster})


def _get_stat_refresh_rate() -> int:
    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
        )
        cur = conn.execute(
            "SELECT value FROM options WHERE key = ?", ("stat_refresh_rate",)
        )
        row = cur.fetchone()
    try:
        rate = int(row[0]) if row else 5
    except (TypeError, ValueError):
        rate = 5
    return max(1, min(rate, 10))


@app.get("/player/stats")
async def player_stats() -> tuple[str, int, dict[str, object]]:
    refresh = _get_stat_refresh_rate()
    player = player_plugins.player.Player()
    _assign_damage_type(player)
    _apply_player_stats(player)
    apply_status_hooks(player)
    stats = {
        "core": {
            "hp": player.hp,
            "max_hp": player.max_hp,
            "exp": player.exp,
            "level": player.level,
            "exp_multiplier": player.exp_multiplier,
            "actions_per_turn": player.actions_per_turn,
        },
        "offense": {
            "atk": player.atk,
            "crit_rate": player.crit_rate,
            "crit_damage": player.crit_damage,
            "effect_hit_rate": player.effect_hit_rate,
            "base_damage_type": getattr(
                player.base_damage_type, "name", str(player.base_damage_type)
            ),
        },
        "defense": {
            "defense": player.defense,
            "mitigation": player.mitigation,
            "regain": player.regain,
            "dodge_odds": player.dodge_odds,
            "effect_resistance": player.effect_resistance,
        },
        "vitality": {"vitality": player.vitality},
        "advanced": {
            "action_points": player.action_points,
            "damage_taken": player.damage_taken,
            "damage_dealt": player.damage_dealt,
            "kills": player.kills,
        },
        "status": {
            "passives": player.passives,
            "dots": player.dots,
            "hots": player.hots,
            "damage_types": player.damage_types,
        },
    }
    return jsonify({"stats": stats, "refresh_rate": refresh})


@app.get("/player/editor")
async def get_player_editor() -> tuple[str, int, dict[str, object]]:
    player = player_plugins.player.Player()
    _assign_damage_type(player)
    pronouns, stats = _load_player_customization()
    return jsonify(
        {
            "pronouns": pronouns,
            "damage_type": getattr(
                player.base_damage_type, "name", player.base_damage_type
            ),
            "hp": stats.get("hp", 0),
            "attack": stats.get("attack", 0),
            "defense": stats.get("defense", 0),
        }
    )


@app.put("/player/editor")
async def update_player_editor() -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    pronouns = (data.get("pronouns") or "").strip()
    damage_type = (data.get("damage_type") or "").capitalize()
    try:
        hp = int(data.get("hp", 0))
        attack = int(data.get("attack", 0))
        defense = int(data.get("defense", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid stats"}), 400
    total = hp + attack + defense

    if len(pronouns) > 15:
        return jsonify({"error": "invalid pronouns"}), 400

    allowed = {"Light", "Dark", "Wind", "Lightning", "Fire", "Ice"}
    if damage_type and damage_type not in allowed:
        return jsonify({"error": "invalid damage type"}), 400

    if total > 100:
        return jsonify({"error": "over-allocation"}), 400

    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
        )
        conn.execute(
            "INSERT OR REPLACE INTO options (key, value) VALUES (?, ?)",
            ("player_pronouns", pronouns),
        )
        conn.execute(
            "INSERT OR REPLACE INTO options (key, value) VALUES (?, ?)",
            (
                "player_stats",
                json.dumps({"hp": hp, "attack": attack, "defense": defense}),
            ),
        )
        if damage_type:
            conn.execute(
                "INSERT OR REPLACE INTO damage_types (id, type) VALUES (?, ?)",
                ("player", damage_type),
            )
    return jsonify({"status": "ok"})


def load_party(run_id: str) -> Party:
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT party FROM runs WHERE id = ?", (run_id,))
        row = cur.fetchone()
    data = json.loads(row[0]) if row else {}
    if isinstance(data, list):
        data = {"members": data, "gold": 0, "relics": [], "cards": []}
    snapshot = data.get("player", {})
    exp_map: dict[str, int] = data.get("exp", {})
    level_map: dict[str, int] = data.get("level", {})
    members: list[PlayerBase] = []
    for pid in data.get("members", []):
        for name in player_plugins.__all__:
            cls = getattr(player_plugins, name)
            if cls.id == pid:
                inst = cls()
                if inst.id == "player":
                    inst.base_damage_type = snapshot.get(
                        "damage_type", inst.base_damage_type
                    )
                    _apply_player_stats(inst, snapshot.get("stats", {}))
                else:
                    _assign_damage_type(inst)
                inst.exp = exp_map.get(pid, 0)
                inst.level = level_map.get(pid, 1)
                members.append(inst)
                break
    party = Party(
        members=members,
        gold=data.get("gold", 0),
        relics=data.get("relics", []),
        cards=data.get("cards", []),
    )
    return party


def load_map(run_id: str) -> tuple[dict, list[MapNode]]:
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT map FROM runs WHERE id = ?", (run_id,))
        row = cur.fetchone()
    if row is None:
        return {"rooms": [], "current": 0, "battle": False}, []
    state = json.loads(row[0])
    rooms = [MapNode.from_dict(n) for n in state.get("rooms", [])]
    return state, rooms


def save_map(run_id: str, state: dict) -> None:
    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "UPDATE runs SET map = ? WHERE id = ?",
            (json.dumps(state), run_id),
        )


def save_party(run_id: str, party: Party) -> None:
    snapshot: dict[str, Any] = {}
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT party FROM runs WHERE id = ?", (run_id,))
        row = cur.fetchone()
    existing = json.loads(row[0]) if row else {}
    snapshot = existing.get("player", {})
    for member in party.members:
        if member.id == "player":
            base = player_plugins.player.Player()
            stats = {
                "hp": int(round((member.max_hp / base.max_hp - 1) * 100)),
                "attack": int(round((member.atk / base.atk - 1) * 100)),
                "defense": int(round((member.defense / base.defense - 1) * 100)),
            }
            snapshot = {
                **snapshot,
                "damage_type": getattr(member.base_damage_type, "id", member.base_damage_type),
                "stats": stats,
            }
            break
    with SAVE_MANAGER.connection() as conn:
        data = {
            "members": [m.id for m in party.members],
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "exp": {m.id: m.exp for m in party.members},
            "level": {m.id: m.level for m in party.members},
            "player": snapshot,
        }
        conn.execute(
            "UPDATE runs SET party = ? WHERE id = ?",
            (json.dumps(data), run_id),
        )


async def _run_battle(
    run_id: str,
    room: BattleRoom,
    party: Party,
    data: dict[str, Any],
    state: dict[str, Any],
    rooms: list[MapNode],
    progress: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    try:
        result = await room.resolve(party, data, progress)
        state["battle"] = False
        has_card_choices = bool(result.get("card_choices"))
        has_relic_choices = bool(result.get("relic_choices"))
        if has_card_choices or has_relic_choices:
            state["awaiting_card"] = has_card_choices
            state["awaiting_relic"] = has_relic_choices
            state["awaiting_next"] = False
            next_type = None
        else:
            state["awaiting_next"] = True
            next_type = (
                rooms[state["current"] + 1].room_type
                if state["current"] + 1 < len(rooms)
                else None
            )
        await asyncio.to_thread(save_map, run_id, state)
        await asyncio.to_thread(save_party, run_id, party)
        result.update(
            {
                "run_id": run_id,
                "action": data.get("action", ""),
                "next_room": next_type,
                "current_room": rooms[state["current"]].room_type,
                "current_index": state["current"],
                "awaiting_card": state.get("awaiting_card", False),
                "awaiting_relic": state.get("awaiting_relic", False),
            }
        )
        battle_snapshots[run_id] = result
    finally:
        battle_tasks.pop(run_id, None)


@app.post("/rooms/<run_id>/battle")
async def battle_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    start = time.perf_counter()
    data = await request.get_json(silent=True) or {}
    action = data.get("action", "")
    party = await asyncio.to_thread(load_party, run_id)
    state, rooms = await asyncio.to_thread(load_map, run_id)
    node = rooms[state["current"]]
    if node.room_type not in {"battle-weak", "battle-normal"}:
        return jsonify({"error": "invalid room"}), 400
    if action == "snapshot":
        snap = battle_snapshots.get(run_id)
        if snap is None:
            return jsonify({"error": "no battle"}), 404
        return jsonify(snap)
    if state.get("awaiting_next"):
        return jsonify({"error": "awaiting next"}), 400
    # If player needs to choose a reward, don't start another battle.
    if state.get("awaiting_card") or state.get("awaiting_relic"):
        # Provide a richer snapshot using the common serializer so the frontend
        # can access fields like base_damage_type for element coloring.
        party_data = [_serialize(m) for m in party.members]
        return jsonify(
            {
                "result": "battle",
                "party": party_data,
                "foes": [],
                "gold": party.gold,
                "relics": party.relics,
                "cards": party.cards,
                "card_choices": [],
                "relic_choices": [],
                "enrage": {"active": False, "stacks": 0},
            }
        )
    if run_id in battle_tasks:
        snap = battle_snapshots.get(run_id, {"result": "battle"})
        app.logger.info(
            "battle_room action=%s %.1fms",
            action,
            (time.perf_counter() - start) * 1000,
        )
        return jsonify(snap)
    state["battle"] = True
    await asyncio.to_thread(save_map, run_id, state)
    room = BattleRoom(node)
    foe = _choose_foe(party)
    _scale_stats(foe, node, room.strength)
    combat_party = Party(
        members=[copy.deepcopy(m) for m in party.members],
        gold=party.gold,
        relics=party.relics,
        cards=party.cards,
    )
    battle_snapshots[run_id] = {
        "result": "battle",
        "party": [_serialize(m) for m in combat_party.members],
        "foes": [_serialize(foe)],
        "gold": party.gold,
        "relics": party.relics,
        "cards": party.cards,
        "card_choices": [],
        "relic_choices": [],
        "enrage": {"active": False, "stacks": 0},
    }

    async def progress(snapshot: dict[str, Any]) -> None:
        battle_snapshots[run_id] = snapshot

    task = asyncio.create_task(
        _run_battle(run_id, room, party, data, state, rooms, progress)
    )
    battle_tasks[run_id] = task
    app.logger.info(
        "battle_room action=%s %.1fms",
        action,
        (time.perf_counter() - start) * 1000,
    )
    return jsonify(battle_snapshots[run_id])


@app.post("/rooms/<run_id>/shop")
async def shop_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type != "shop":
        return jsonify({"error": "invalid room"}), 400
    if state.get("awaiting_next"):
        return jsonify({"error": "awaiting next"}), 400
    room = ShopRoom(node)
    result = await room.resolve(party, data)
    if data.get("action") == "leave":
        state["awaiting_next"] = True
        next_type = (
            rooms[state["current"] + 1].room_type
            if state["current"] + 1 < len(rooms)
            else None
        )
    else:
        state["awaiting_next"] = False
        next_type = None
    save_map(run_id, state)
    save_party(run_id, party)
    result.update(
        {
            "run_id": run_id,
            "action": data.get("action", ""),
            "next_room": next_type,
            "current_room": node.room_type,
            "current_index": state["current"],
            "awaiting_card": state.get("awaiting_card", False),
            "awaiting_relic": state.get("awaiting_relic", False),
        }
    )
    return jsonify(result)


@app.post("/rooms/<run_id>/rest")
async def rest_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type != "rest":
        return jsonify({"error": "invalid room"}), 400
    if state.get("awaiting_next"):
        return jsonify({"error": "awaiting next"}), 400
    room = RestRoom(node)
    result = await room.resolve(party, data)
    if data.get("action") == "leave":
        state["awaiting_next"] = True
        next_type = (
            rooms[state["current"] + 1].room_type
            if state["current"] + 1 < len(rooms)
            else None
        )
    else:
        state["awaiting_next"] = False
        next_type = None
    save_map(run_id, state)
    save_party(run_id, party)
    result.update(
        {
            "run_id": run_id,
            "action": data.get("action", ""),
            "next_room": next_type,
            "current_room": node.room_type,
            "current_index": state["current"],
            "awaiting_card": state.get("awaiting_card", False),
            "awaiting_relic": state.get("awaiting_relic", False),
        }
    )
    return jsonify(result)


@app.post("/rooms/<run_id>/chat")
async def chat_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type != "chat":
        return jsonify({"error": "invalid room"}), 400
    if state.get("awaiting_next"):
        return jsonify({"error": "awaiting next"}), 400
    room = ChatRoom(node)
    result = await room.resolve(party, data)
    state["awaiting_next"] = True
    next_type = (
        rooms[state["current"] + 1].room_type
        if state["current"] + 1 < len(rooms)
        else None
    )
    save_map(run_id, state)
    save_party(run_id, party)
    result.update(
        {
            "run_id": run_id,
            "action": data.get("action", ""),
            "next_room": next_type,
            "current_room": node.room_type,
            "current_index": state["current"],
            "awaiting_card": state.get("awaiting_card", False),
            "awaiting_relic": state.get("awaiting_relic", False),
        }
    )
    return jsonify(result)


@app.post("/rooms/<run_id>/boss")
async def boss_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type != "battle-boss-floor":
        return jsonify({"error": "invalid room"}), 400
    # Prevent starting a boss battle while awaiting a card selection or next-room trigger
    if state.get("awaiting_card") or state.get("awaiting_relic") or state.get("awaiting_next"):
        party_data = [
            {
                "id": m.id,
                "name": getattr(m, "name", m.id),
                "hp": m.hp,
                "max_hp": m.max_hp,
                "atk": m.atk,
                "hots": getattr(m, "hots", []),
                "dots": getattr(m, "dots", []),
            }
            for m in party.members
        ]
        return jsonify({
            "result": "boss",
            "party": party_data,
            "foes": [],
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "card_choices": [],
            "enrage": {"active": False, "stacks": 0},
        })
    state["battle"] = True
    save_map(run_id, state)
    room = BossRoom(node)
    result = await room.resolve(party, data)
    state["battle"] = False
    has_card_choices = bool(result.get("card_choices"))
    has_relic_choices = bool(result.get("relic_choices"))
    if has_card_choices or has_relic_choices:
        state["awaiting_card"] = has_card_choices
        state["awaiting_relic"] = has_relic_choices
        state["awaiting_next"] = False
        next_type = None
    else:
        state["awaiting_next"] = True
        next_type = (
            rooms[state["current"] + 1].room_type
            if state["current"] + 1 < len(rooms)
            else None
        )
    save_map(run_id, state)
    save_party(run_id, party)
    result.update(
        {"run_id": run_id, "action": data.get("action", ""), "next_room": next_type}
    )
    return jsonify(result)


@app.post("/cards/<run_id>")
async def select_card(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    card_id = data.get("card")
    if not card_id:
        return jsonify({"error": "invalid card"}), 400
    party = load_party(run_id)
    card = award_card(party, card_id)
    if card is None:
        return jsonify({"error": "invalid card"}), 400
    # Advance the map now that the player chose a reward
    state, rooms = load_map(run_id)
    state["awaiting_card"] = False
    if not state.get("awaiting_relic"):
        state["awaiting_next"] = True
        next_type = (
            rooms[state["current"] + 1].room_type
            if state["current"] + 1 < len(rooms)
            else None
        )
    else:
        state["awaiting_next"] = False
        next_type = None
    save_map(run_id, state)
    save_party(run_id, party)
    card_data = {"id": card.id, "name": card.name, "stars": card.stars}
    return jsonify({"card": card_data, "cards": party.cards, "next_room": next_type})


@app.post("/relics/<run_id>")
async def select_relic(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    relic_id = data.get("relic")
    if not relic_id:
        return jsonify({"error": "invalid relic"}), 400
    party = load_party(run_id)
    relic = award_relic(party, relic_id)
    if relic is None:
        return jsonify({"error": "invalid relic"}), 400
    state, rooms = load_map(run_id)
    state["awaiting_relic"] = False
    if not state.get("awaiting_card"):
        state["awaiting_next"] = True
        next_type = (
            rooms[state["current"] + 1].room_type
            if state["current"] + 1 < len(rooms)
            else None
        )
    else:
        state["awaiting_next"] = False
        next_type = None
    save_map(run_id, state)
    save_party(run_id, party)
    relic_data = {"id": relic.id, "name": relic.name, "stars": relic.stars}
    return jsonify({"relic": relic_data, "relics": party.relics, "next_room": next_type})


@app.post("/run/<run_id>/next")
async def advance_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    state, rooms = load_map(run_id)
    if state.get("awaiting_card") or state.get("awaiting_relic"):
        return jsonify({"error": "awaiting reward"}), 400
    if not state.get("awaiting_next"):
        return jsonify({"error": "not ready"}), 400
    state["current"] += 1
    state["awaiting_next"] = False
    next_type = (
        rooms[state["current"]].room_type if state["current"] < len(rooms) else None
    )
    save_map(run_id, state)
    return jsonify({"next_room": next_type, "current_index": state["current"]})


@app.post("/rooms/<run_id>/<room_id>/action")
async def room_action(run_id: str, room_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    return jsonify(
        {"run_id": run_id, "room_id": room_id, "action": data.get("action", "noop")}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=59002)

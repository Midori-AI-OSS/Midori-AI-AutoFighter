from __future__ import annotations

import json

from uuid import uuid4
from pathlib import Path
from dataclasses import asdict

from quart import Quart
from quart import jsonify
from quart import request
from quart import send_from_directory

from plugins import passives as passive_plugins
from plugins import players as player_plugins
from autofighter.cards import award_card
from autofighter.party import Party
from autofighter.rooms import BattleRoom, BossRoom, ChatRoom, RestRoom, ShopRoom
from autofighter.stats import apply_status_hooks
from autofighter.gacha import GachaManager
from autofighter.mapgen import MapGenerator, MapNode
from plugins.players._base import PlayerBase
from autofighter.save_manager import SaveManager


SAVE_MANAGER = SaveManager.from_env()
SAVE_MANAGER.migrate(Path(__file__).resolve().parent / "migrations")
with SAVE_MANAGER.connection() as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS damage_types (id TEXT PRIMARY KEY, type TEXT)"
    )

app = Quart(__name__)


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
        cur = conn.execute(
            "SELECT type FROM damage_types WHERE id = ?", (player.id,)
        )
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
        cur = conn.execute(
            "SELECT value FROM options WHERE key = ?", ("player_stats",)
        )
        row = cur.fetchone()
        if row:
            try:
                stats.update(json.loads(row[0]))
            except (TypeError, ValueError, json.JSONDecodeError):
                pass
    return pronouns, stats


def _apply_player_stats(player: PlayerBase) -> None:
    _pronouns, stats = _load_player_customization()
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
    state = {"rooms": [n.to_dict() for n in nodes], "current": 1}
    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "INSERT INTO runs (id, party, map) VALUES (?, ?, ?)",
            (
                run_id,
                json.dumps({"members": members, "gold": 0, "relics": [], "cards": []}),
                json.dumps(state),
            ),
        )

    party_info: list[dict[str, object]] = []
    for pid in members:
        for name in player_plugins.__all__:
            cls = getattr(player_plugins, name)
            if cls.id == pid:
                inst = cls()
                _assign_damage_type(inst)
                party_info.append(
                    {
                        "id": inst.id,
                        "name": inst.name,
                        "passives": _passive_names(getattr(inst, "passives", [])),
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
    party = {"members": members, "gold": gold, "relics": relics, "cards": cards}
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
            "damage_type": getattr(player.base_damage_type, "name", player.base_damage_type),
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

    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM runs")
        if cur.fetchone()[0]:
            return jsonify({"error": "run active"}), 400

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
            ("player_stats", json.dumps({"hp": hp, "attack": attack, "defense": defense})),
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
    members: list[PlayerBase] = []
    for pid in data.get("members", []):
        for name in player_plugins.__all__:
            cls = getattr(player_plugins, name)
            if cls.id == pid:
                inst = cls()
                _assign_damage_type(inst)
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
        return {"rooms": [], "current": 0}, []
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
    with SAVE_MANAGER.connection() as conn:
        data = {
            "members": [m.id for m in party.members],
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
        }
        conn.execute(
            "UPDATE runs SET party = ? WHERE id = ?",
            (json.dumps(data), run_id),
        )


@app.post("/rooms/<run_id>/battle")
async def battle_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type not in {"battle-weak", "battle-normal"}:
        return jsonify({"error": "invalid room"}), 400
    room = BattleRoom(node)
    result = room.resolve(party, data)
    state["current"] += 1
    save_map(run_id, state)
    save_party(run_id, party)
    result.update({"run_id": run_id, "action": data.get("action", "")})
    return jsonify(result)


@app.post("/rooms/<run_id>/shop")
async def shop_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type != "shop":
        return jsonify({"error": "invalid room"}), 400
    room = ShopRoom(node)
    result = room.resolve(party, data)
    state["current"] += 1
    save_map(run_id, state)
    save_party(run_id, party)
    result.update({"run_id": run_id, "action": data.get("action", "")})
    return jsonify(result)


@app.post("/rooms/<run_id>/rest")
async def rest_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type != "rest":
        return jsonify({"error": "invalid room"}), 400
    room = RestRoom(node)
    result = room.resolve(party, data)
    state["current"] += 1
    save_map(run_id, state)
    save_party(run_id, party)
    result.update({"run_id": run_id, "action": data.get("action", "")})
    return jsonify(result)


@app.post("/rooms/<run_id>/chat")
async def chat_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type != "chat":
        return jsonify({"error": "invalid room"}), 400
    room = ChatRoom(node)
    result = room.resolve(party, data)
    state["current"] += 1
    save_map(run_id, state)
    save_party(run_id, party)
    result.update({"run_id": run_id, "action": data.get("action", "")})
    return jsonify(result)


@app.post("/rooms/<run_id>/boss")
async def boss_room(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = load_party(run_id)
    state, rooms = load_map(run_id)
    node = rooms[state["current"]]
    if node.room_type != "battle-boss-floor":
        return jsonify({"error": "invalid room"}), 400
    room = BossRoom(node)
    result = room.resolve(party, data)
    state["current"] += 1
    save_map(run_id, state)
    save_party(run_id, party)
    result.update({"run_id": run_id, "action": data.get("action", "")})
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
    save_party(run_id, party)
    card_data = {"id": card.id, "name": card.name, "stars": card.stars}
    return jsonify({"card": card_data, "cards": party.cards})


@app.post("/rooms/<run_id>/<room_id>/action")
async def room_action(run_id: str, room_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    return jsonify({"run_id": run_id, "room_id": room_id, "action": data.get("action", "noop")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=59002)

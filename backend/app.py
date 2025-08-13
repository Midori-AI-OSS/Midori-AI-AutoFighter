from __future__ import annotations

import os
import json

from uuid import uuid4
from pathlib import Path
from dataclasses import asdict

from quart import Quart
from quart import request
from quart import jsonify
from quart import send_from_directory

from autofighter.mapgen import MapGenerator, MapNode
from autofighter.rooms import BattleRoom, BossRoom, ChatRoom, RestRoom, ShopRoom
from autofighter.save_manager import SaveManager
from plugins import players as player_plugins


SAVE_MANAGER = SaveManager.from_env()
SAVE_MANAGER.migrate(Path(__file__).resolve().parent / "migrations")

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


@app.post("/run/start")
async def start_run() -> tuple[str, int, dict[str, str]]:
    run_id = str(uuid4())
    generator = MapGenerator(run_id)
    nodes = generator.generate_floor()
    state = {"rooms": [n.to_dict() for n in nodes], "current": 1}
    with SAVE_MANAGER.connection() as conn:
        conn.execute(
            "INSERT INTO runs (id, party, map) VALUES (?, ?, ?)",
            (run_id, json.dumps([]), json.dumps(state)),
        )
    return jsonify({"run_id": run_id, "map": state})


@app.put("/party/<run_id>")
async def update_party(run_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    party = data.get("party", [])
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


def load_party(run_id: str) -> list[player_plugins.PlayerBase]:
    with SAVE_MANAGER.connection() as conn:
        cur = conn.execute("SELECT party FROM runs WHERE id = ?", (run_id,))
        row = cur.fetchone()
    party_ids = json.loads(row[0]) if row else []
    members: list[player_plugins.PlayerBase] = []
    for pid in party_ids:
        for name in player_plugins.__all__:
            cls = getattr(player_plugins, name)
            if cls.id == pid:
                members.append(cls())
                break
    return members


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
    result.update({"run_id": run_id, "action": data.get("action", "")})
    return jsonify(result)


@app.post("/rooms/<run_id>/<room_id>/action")
async def room_action(run_id: str, room_id: str) -> tuple[str, int, dict[str, str]]:
    data = await request.get_json(silent=True) or {}
    return jsonify({"run_id": run_id, "room_id": room_id, "action": data.get("action", "noop")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=59002)

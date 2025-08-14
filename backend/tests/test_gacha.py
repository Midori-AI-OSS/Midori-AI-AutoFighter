from pathlib import Path
from unittest.mock import patch

import pytest
import sqlcipher3
import importlib.util


@pytest.fixture()
def app_with_db(tmp_path, monkeypatch):
    db_path = tmp_path / "save.db"
    monkeypatch.setenv("AF_DB_PATH", str(db_path))
    monkeypatch.setenv("AF_DB_KEY", "testkey")
    monkeypatch.syspath_prepend(Path(__file__).resolve().parents[1])
    spec = importlib.util.spec_from_file_location(
        "app", Path(__file__).resolve().parents[1] / "app.py",
    )
    app_module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(app_module)
    app_module.app.testing = True
    return app_module.app, db_path


@pytest.mark.asyncio
async def test_pull_items(app_with_db):
    app, _ = app_with_db
    client = app.test_client()

    with patch(
        "autofighter.gacha.random.random", side_effect=[0.5, 1.0, 0.99]
    ), patch("autofighter.gacha.random.choice", return_value="fire"):
        resp = await client.post("/gacha/pull", json={"count": 1})
    data = await resp.get_json()
    assert data["pity"] == 1
    assert data["results"][0]["type"] == "item"
    assert data["results"][0]["rarity"] == 4
    assert data["items"]["fire_4"] == 1


@pytest.mark.asyncio
async def test_pull_five_star_duplicate(app_with_db):
    app, db_path = app_with_db
    client = app.test_client()

    with patch(
        "autofighter.gacha.random.random", side_effect=[0.5, 0.0]
    ), patch("autofighter.gacha.random.choice", return_value="becca"):
        resp = await client.post("/gacha/pull", json={"count": 1})
    data = await resp.get_json()
    assert data["pity"] == 0
    assert data["results"][0]["rarity"] == 5
    char_id = data["results"][0]["id"]

    from autofighter.gacha import FIVE_STAR

    conn = sqlcipher3.connect(db_path)
    conn.execute("PRAGMA key = 'testkey'")
    others = [cid for cid in FIVE_STAR if cid != char_id]
    for cid in others:
        conn.execute("INSERT INTO owned_players (id) VALUES (?)", (cid,))
    conn.commit()

    with patch(
        "autofighter.gacha.random.random", side_effect=[0.5, 0.0]
    ), patch("autofighter.gacha.random.choice", return_value=char_id):
        resp = await client.post("/gacha/pull", json={"count": 1})
    data = await resp.get_json()
    for player in data["players"]:
        if player["id"] == char_id:
            assert player["stacks"] == 2
            break
    else:
        pytest.fail("character not found")

    cur = conn.execute(
        "SELECT stacks FROM player_stacks WHERE id = ?", (char_id,)
    )
    assert cur.fetchone()[0] == 2


@pytest.mark.asyncio
async def test_pull_six_star(app_with_db):
    app, _ = app_with_db
    client = app.test_client()

    with patch(
        "autofighter.gacha.random.random", return_value=0.0
    ), patch(
        "autofighter.gacha.random.choice", return_value="lady_fire_and_ice"
    ):
        resp = await client.post("/gacha/pull", json={"count": 1})
    data = await resp.get_json()
    assert data["pity"] == 0
    assert data["results"][0]["rarity"] == 6
    assert data["results"][0]["id"] == "lady_fire_and_ice"


@pytest.mark.asyncio
async def test_auto_craft_setting(app_with_db):
    app, db_path = app_with_db
    client = app.test_client()
    conn = sqlcipher3.connect(db_path)
    conn.execute("PRAGMA key = 'testkey'")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
    )
    conn.execute(
        "INSERT OR REPLACE INTO options (key, value) VALUES (?, ?)",
        ("upgrade_items", '{"fire_1":125}')
    )
    conn.commit()
    with patch(
        "autofighter.gacha.random.random", side_effect=[0.5, 1.0, 0.0]
    ), patch("autofighter.gacha.random.choice", return_value="fire"):
        resp = await client.post("/gacha/pull", json={"count": 1})
    data = await resp.get_json()
    assert data["items"]["fire_1"] == 126
    assert "fire_2" not in data["items"]

    resp = await client.post("/gacha/auto-craft", json={"enabled": True})
    assert (await resp.get_json())["auto_craft"] is True
    conn.execute(
        "INSERT OR REPLACE INTO options (key, value) VALUES (?, ?)",
        ("upgrade_items", '{"fire_1":125}')
    )
    conn.commit()
    with patch(
        "autofighter.gacha.random.random", side_effect=[0.5, 1.0, 0.0]
    ), patch("autofighter.gacha.random.choice", return_value="fire"):
        resp = await client.post("/gacha/pull", json={"count": 1})
    data = await resp.get_json()
    assert data["items"]["fire_1"] == 1
    assert data["items"]["fire_2"] == 1


@pytest.mark.asyncio
async def test_manual_craft_endpoint(app_with_db):
    app, db_path = app_with_db
    client = app.test_client()
    conn = sqlcipher3.connect(db_path)
    conn.execute("PRAGMA key = 'testkey'")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)",
    )
    conn.execute(
        "INSERT OR REPLACE INTO options (key, value) VALUES (?, ?)",
        ("upgrade_items", '{"fire_1":125}')
    )
    conn.commit()
    resp = await client.post("/gacha/craft")
    data = await resp.get_json()
    assert data["items"].get("fire_1", 0) == 0
    assert data["items"]["fire_2"] == 1


@pytest.mark.asyncio
async def test_pity_scales_item_rarity(app_with_db):
    app, db_path = app_with_db
    client = app.test_client()
    conn = sqlcipher3.connect(db_path)
    conn.execute("PRAGMA key = 'testkey'")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
    )
    conn.execute(
        "INSERT OR REPLACE INTO options (key, value) VALUES ('gacha_pity', '178')"
    )
    conn.commit()
    with patch(
        "autofighter.gacha.random.random", side_effect=[0.5, 0.99, 0.05]
    ), patch("autofighter.gacha.random.choice", return_value="fire"):
        resp = await client.post("/gacha/pull", json={"count": 1})
    data = await resp.get_json()
    assert data["results"][0]["rarity"] >= 2

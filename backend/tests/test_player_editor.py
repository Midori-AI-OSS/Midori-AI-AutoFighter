import importlib.util
from pathlib import Path

import pytest
import sqlcipher3


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
async def test_player_editor_update_and_fetch(app_with_db):
    app, db_path = app_with_db
    client = app.test_client()

    resp = await client.put(
        "/player/editor",
        json={
            "pronouns": "they",
            "damage_type": "Fire",
            "hp": 10,
            "attack": 20,
            "defense": 30,
        },
    )
    assert resp.status_code == 200

    data = await client.get("/player/editor")
    payload = await data.get_json()
    assert payload == {
        "pronouns": "they",
        "damage_type": "Fire",
        "hp": 10,
        "attack": 20,
        "defense": 30,
    }

    stats_resp = await client.get("/player/stats")
    stats_payload = await stats_resp.get_json()
    core = stats_payload["stats"]["core"]
    offense = stats_payload["stats"]["offense"]
    defense_block = stats_payload["stats"]["defense"]
    assert core["hp"] == 1100 and core["max_hp"] == 1100
    assert offense["atk"] == 120
    assert defense_block["defense"] == 65

    conn = sqlcipher3.connect(db_path)
    conn.execute("PRAGMA key = 'testkey'")
    cur = conn.execute("SELECT type FROM damage_types WHERE id = ?", ("player",))
    assert cur.fetchone()[0] == "Fire"


@pytest.mark.asyncio
async def test_player_editor_validation(app_with_db):
    app, _ = app_with_db
    client = app.test_client()

    resp = await client.put(
        "/player/editor",
        json={
            "pronouns": "x" * 16,
            "damage_type": "Generic",
            "hp": 200,
            "attack": 0,
            "defense": 0,
        },
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_player_editor_blocked_during_run(app_with_db):
    app, db_path = app_with_db
    client = app.test_client()

    await client.post("/run/start", json={"party": ["player"]})
    resp = await client.put(
        "/player/editor",
        json={"pronouns": "they", "hp": 1, "attack": 1, "defense": 1},
    )
    assert resp.status_code == 400

    conn = sqlcipher3.connect(db_path)
    conn.execute("PRAGMA key = 'testkey'")
    conn.execute("DELETE FROM runs")
    conn.commit()

    resp2 = await client.put(
        "/player/editor",
        json={"pronouns": "they", "hp": 1, "attack": 1, "defense": 1},
    )
    assert resp2.status_code == 200

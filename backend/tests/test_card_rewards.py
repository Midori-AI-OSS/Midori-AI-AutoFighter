import json
import importlib.util

import pytest
import sqlcipher3

import autofighter.cards as cards_module

from pathlib import Path
from autofighter.cards import award_card
from autofighter.party import Party
from autofighter.stats import Stats

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


def test_award_card_unique():
    member = Stats()
    member.id = "m1"
    party = Party(members=[member])
    assert award_card(party, "micro_blade") is not None
    assert award_card(party, "micro_blade") is None
    assert party.cards == ["micro_blade"]


@pytest.mark.asyncio
async def test_battle_offers_choices_and_applies_effect(app_with_db, monkeypatch):
    app, db_path = app_with_db
    client = app.test_client()

    start_resp = await client.post("/run/start", json={"party": ["player"]})
    run_id = (await start_resp.get_json())["run_id"]
    await client.put(f"/party/{run_id}", json={"party": ["player"]})

    monkeypatch.setattr(cards_module.random, "sample", lambda seq, k: list(seq)[:k])

    battle_resp = await client.post(f"/rooms/{run_id}/battle")
    data = await battle_resp.get_json()
    assert data["party"][0]["atk"] == 100
    chosen = data["card_choices"][0]["id"]

    await client.post(f"/cards/{run_id}", json={"card": chosen})
    while True:
        map_resp = await client.get(f"/map/{run_id}")
        map_state = (await map_resp.get_json())["map"]
        node = map_state["rooms"][map_state["current"]]
        room_type = node["room_type"]
        if room_type in {"battle-weak", "battle-normal"}:
            break
        if room_type == "shop":
            await client.post(f"/rooms/{run_id}/shop")
        elif room_type == "rest":
            await client.post(f"/rooms/{run_id}/rest")
        else:
            raise AssertionError(f"unexpected room type: {room_type}")

    battle_resp2 = await client.post(f"/rooms/{run_id}/battle")
    data2 = await battle_resp2.get_json()
    atk = next(p for p in data2["party"] if p["id"] == "player")["atk"]
    effect = cards_module._registry()[chosen]().effects.get("atk", 0)
    assert atk == int(100 * (1 + effect))

    conn = sqlcipher3.connect(db_path)
    conn.execute("PRAGMA key = 'testkey'")
    row = conn.execute("SELECT party FROM runs WHERE id = ?", (run_id,)).fetchone()
    saved = json.loads(row[0])
    assert chosen in saved["cards"]

import json
import random
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


def test_award_card_unique():
    from autofighter.cards import award_card
    from autofighter.party import Party
    from autofighter.stats import Stats

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

    start_resp = await client.post("/run/start")
    run_id = (await start_resp.get_json())["run_id"]
    await client.put(f"/party/{run_id}", json={"party": ["player"]})

    monkeypatch.setattr(random, "sample", lambda seq, k: list(seq)[:k])

    battle_resp = await client.post(f"/rooms/{run_id}/battle")
    data = await battle_resp.get_json()
    assert data["party"][0]["atk"] == 100
    assert any(c["id"] == "micro_blade" for c in data["card_choices"])

    await client.post(f"/cards/{run_id}", json={"card": "micro_blade"})

    battle_resp2 = await client.post(f"/rooms/{run_id}/battle")
    data2 = await battle_resp2.get_json()
    atk = next(p for p in data2["party"] if p["id"] == "player")["atk"]
    assert atk == int(100 * 1.03)

    conn = sqlcipher3.connect(db_path)
    conn.execute("PRAGMA key = 'testkey'")
    row = conn.execute("SELECT party FROM runs WHERE id = ?", (run_id,)).fetchone()
    saved = json.loads(row[0])
    assert "micro_blade" in saved["cards"]

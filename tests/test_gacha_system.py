from __future__ import annotations

import random
from pathlib import Path
from unittest.mock import patch

import pytest

from autofighter.gacha.system import GachaSystem
from autofighter.gacha.vitality import vitality_bonus


def count_player_plugins() -> int:
    path = Path("plugins/players")
    return len([p for p in path.glob("*.py") if p.name != "__init__.py"])


def test_seeded_pool_matches_plugins() -> None:
    gs = GachaSystem()
    assert len(gs.pool) == count_player_plugins()


def test_failed_pull_grants_item() -> None:
    gs = GachaSystem(rng=random.Random(0))
    with patch.object(gs.rng, "random", return_value=0.9):
        result = gs.pull(1)
    assert result.characters == []
    assert result.upgrade_items[1] == 1


def test_duplicate_vitality_stack() -> None:
    gs = GachaSystem(rng=random.Random(0))
    with patch.object(gs.rng, "random", return_value=0.0), patch.object(
        gs.rng, "choice", return_value="ally"
    ):
        gs.pull(1)
        result = gs.pull(1)
    assert gs.owned["ally"] == 2
    assert result.vitality["ally"] == vitality_bonus(1)


def test_serialization_round_trip() -> None:
    gs = GachaSystem(rng=random.Random(0))
    with patch.object(gs.rng, "random", return_value=0.0), patch.object(
        gs.rng, "choice", return_value="ally"
    ):
        gs.pull(1)
    gs.upgrade_items[1] = 2
    gs.tickets = 1
    data = gs.serialize()
    loaded = GachaSystem.deserialize(data, rng=random.Random(0))
    assert loaded.owned == gs.owned
    assert loaded.upgrade_items == gs.upgrade_items
    assert loaded.tickets == gs.tickets
    assert loaded.pity_5 == gs.pity_5
    assert loaded.pity_6 == gs.pity_6


def test_crafting_converts_on_pull() -> None:
    gs = GachaSystem(rng=random.Random(0))
    gs.upgrade_items[1] = 124
    with patch.object(gs.rng, "random", return_value=0.9):
        result = gs.pull(1)
    assert gs.upgrade_items[1] == 0
    assert gs.upgrade_items[2] == 1
    assert result.upgrade_items[2] == 1


def test_trade_for_tickets() -> None:
    gs = GachaSystem(rng=random.Random(0))
    gs.upgrade_items[4] = 10
    with patch.object(gs.rng, "random", return_value=0.9):
        result = gs.pull(1)
    assert gs.tickets == 1
    assert gs.upgrade_items[4] == 0
    assert result.tickets == 1


def test_pity_counters_increment() -> None:
    gs = GachaSystem(rng=random.Random(0))
    with patch.object(gs.rng, "random", return_value=0.99):
        gs.pull(1)
    assert gs.pity_5 == 1
    assert gs.pity_6 == 1


def test_pity_resets_on_feature_drop() -> None:
    gs = GachaSystem(rng=random.Random(0))
    gs.pity_5 = 179
    with patch.object(gs.rng, "random", return_value=0.99), patch.object(
        gs.rng, "choice", return_value="ally"
    ):
        gs.pull(1)
    assert gs.pity_5 == 0
    assert gs.pity_6 == 1


def test_pity_resets_on_six_star() -> None:
    gs = GachaSystem(rng=random.Random(0))
    gs.pity_6 = 2000
    with patch.object(gs.rng, "random", return_value=0.99), patch.object(
        gs.rng, "choice", return_value="ally"
    ):
        gs.pull(1)
    assert gs.pity_5 == 0
    assert gs.pity_6 == 0


def test_stat_bonus_applied() -> None:
    gs = GachaSystem(rng=random.Random(0))
    plugin = gs.players["ally"]
    plugin.stat_bonuses = {"atk": 10}
    try:
        with patch.object(gs.rng, "random", return_value=0.0), patch.object(
            gs.rng, "choice", return_value="ally",
        ):
            gs.pull(1)
            r2 = gs.pull(1)
            r3 = gs.pull(1)
        assert r2.stats["ally"]["atk"] == pytest.approx(10)
        assert r3.stats["ally"]["atk"] == pytest.approx(10 * 1.05)
        assert gs.owned["ally"] == 3
    finally:
        delattr(plugin, "stat_bonuses")

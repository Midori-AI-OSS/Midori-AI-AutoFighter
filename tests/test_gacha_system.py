from __future__ import annotations

import random
from pathlib import Path
from unittest.mock import patch

from autofighter.gacha.system import GachaSystem
from autofighter.gacha.vitality import vitality_bonus


def count_player_plugins() -> int:
    path = Path("plugins/players")
    return len([p for p in path.glob("*.py") if p.name != "__init__.py"])


class FixedRandom:
    def random(self) -> float:
        return 0.999999

    def choice(self, seq):
        return seq[0]


def test_seeded_pool_matches_plugins() -> None:
    gs = GachaSystem()
    assert len(gs.pool) == count_player_plugins()


def test_failed_pull_grants_item() -> None:
    gs = GachaSystem(rng=random.Random(0))
    with patch.object(gs.rng, "random", return_value=0.9):
        result = gs.pull(1)
    assert result.characters == []
    assert result.upgrade_items == 1


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
    data = gs.serialize()
    loaded = GachaSystem.deserialize(data, rng=random.Random(0))
    assert loaded.owned == gs.owned


def test_pity_rate_escalates() -> None:
    gs = GachaSystem(rng=FixedRandom())
    for _ in range(gs.soft_pity - 1):
        gs.pull(1)
    assert gs.pity_counter == gs.soft_pity - 1
    assert gs.current_rate() == gs.base_rate
    gs.pull(1)
    assert gs.pity_counter == gs.soft_pity
    assert gs.current_rate() > gs.base_rate


def test_hard_pity_guarantees_character() -> None:
    gs = GachaSystem(rng=FixedRandom())
    for _ in range(gs.hard_pity - 1):
        result = gs.pull(1)
        assert result.characters == []
    result = gs.pull(1)
    assert len(result.characters) == 1
    assert gs.pity_counter == 0


def test_pity_serialization_persists() -> None:
    gs = GachaSystem(rng=FixedRandom())
    for _ in range(10):
        gs.pull(1)
    data = gs.serialize()
    loaded = GachaSystem.deserialize(data, rng=FixedRandom())
    assert loaded.pity_counter == gs.pity_counter

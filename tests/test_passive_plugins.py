import sys
import types
import random
from pathlib import Path

import pytest

halo_stub = types.ModuleType("halo")


class DummyHalo:
    def __init__(self, *args, **kwargs) -> None:  # noqa: D401
        """Stand-in for the Halo spinner."""


halo_stub.Halo = DummyHalo
sys.modules.setdefault("halo", halo_stub)

colorama_stub = types.ModuleType("colorama")


class DummyColor:
    def __getattr__(self, _) -> str:  # noqa: D401
        """Return empty string for any attribute."""

        return ""


colorama_stub.Fore = DummyColor()
colorama_stub.Style = DummyColor()
sys.modules.setdefault("colorama", colorama_stub)

pygame_stub = types.ModuleType("pygame")
pygame_stub.image = types.SimpleNamespace(load=lambda *args, **kwargs: object())
sys.modules.setdefault("pygame", pygame_stub)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from damagestate import check_passive_mod
from damagetypes import Generic
from passives import get_passive
from player import Player


def test_bleeding_blow_applies_bleed() -> None:
    passive = get_passive("bleeding_blow")
    assert passive is not None
    source = Player("Hero")
    source.Type = Generic
    target = Player("Foe")
    passive.on_apply(source)
    source.BleedChance = 1.0
    random.seed(0)
    pre_dots = len(target.DOTS)
    mited_damage = source.deal_damage(1, target.Type)
    check_passive_mod([target], [source], source, target, mited_damage)
    assert len(target.DOTS) == pre_dots + 1
    assert target.DOTS[0].name == "Bleed"


def test_get_passive_handles_missing_dir(tmp_path: Path) -> None:
    missing = tmp_path / "no_plugins"
    passive = get_passive("bleeding_blow", plugin_dir=str(missing))
    assert passive is None

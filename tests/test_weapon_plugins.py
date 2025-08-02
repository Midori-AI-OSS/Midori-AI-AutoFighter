import sys
import types
import shutil

from pathlib import Path

import pytest


halo_stub = types.ModuleType("halo")


class DummyHalo:
    def __init__(self, *args, **kwargs) -> None:
        """Stand-in for the Halo spinner."""


halo_stub.Halo = DummyHalo
sys.modules.setdefault("halo", halo_stub)

colorama_stub = types.ModuleType("colorama")


class DummyColor:
    def __getattr__(self, _):
        """Return empty string for any attribute."""

        return ""


colorama_stub.Fore = DummyColor()
colorama_stub.Style = DummyColor()
sys.modules.setdefault("colorama", colorama_stub)

pygame_stub = types.ModuleType("pygame")
pygame_stub.image = types.SimpleNamespace(load=lambda *args, **kwargs: object())
sys.modules.setdefault("pygame", pygame_stub)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from player import Player
from weapons import WeaponType, get_weapon
from damagetypes import Generic
from plugins.plugin_loader import PluginLoader


def test_sword_attack_deals_damage():
    loader = PluginLoader()
    loader.discover("plugins/weapons")
    sword_cls = loader.get_plugins("weapon")["sword"]

    attacker = Player("Hero")
    attacker.Type = Generic
    target = Player("Foe")
    target.Type = Generic
    target.DodgeOdds = 0
    target.Def = 1

    weapon = sword_cls()
    starting_hp = target.HP
    damage = weapon.attack(attacker, target)

    assert damage > 0
    assert target.HP < starting_hp


def test_staff_attack_deals_damage():
    loader = PluginLoader()
    loader.discover("plugins/weapons")
    staff_cls = loader.get_plugins("weapon")["staff"]

    attacker = Player("Hero")
    attacker.Type = Generic
    target = Player("Foe")
    target.Type = Generic
    target.DodgeOdds = 0
    target.Def = 1

    weapon = staff_cls()
    starting_hp = target.HP
    damage = weapon.attack(attacker, target)

    assert damage > 0
    assert target.HP < starting_hp


def test_weapon_fallback_without_plugins(tmp_path):
    root = Path(__file__).resolve().parents[1]
    weapons_dir = root / "plugins" / "weapons"
    backup = tmp_path / "weapons"
    shutil.move(weapons_dir, backup)
    try:
        weapon = get_weapon("sword")
        assert isinstance(weapon, WeaponType)
        assert weapon.name == "Sword"
    finally:
        shutil.move(backup, weapons_dir)


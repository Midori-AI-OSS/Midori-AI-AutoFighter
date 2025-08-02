import sys
import types

colorama_stub = types.ModuleType("colorama")


class DummyColor:
    def __getattr__(self, _):
        return ""


colorama_stub.Fore = DummyColor()
colorama_stub.Style = DummyColor()
sys.modules.setdefault("colorama", colorama_stub)

from healing_over_time import get_hot, hot
from plugins.plugin_loader import PluginLoader


class DummyTarget:
    def __init__(self, hp: int = 50, mhp: int = 100) -> None:
        self.HP = hp
        self.MHP = mhp


def test_regeneration_heals_over_time():
    loader = PluginLoader()
    loader.discover("plugins")
    plugin_cls = loader.get_plugins("hot")["regeneration"]
    target = DummyTarget()
    effect = plugin_cls(healing=10, turns=2)
    starting_hp = target.HP

    assert effect.tick(target, 1) is True
    assert target.HP == starting_hp + 10

    assert effect.tick(target, 1) is False
    assert target.HP == starting_hp + 20


def test_hot_fallback_when_missing(tmp_path):
    effect = get_hot(
        "missing",
        plugin_dir=str(tmp_path),
        name="Fallback",
        healing=1,
        turns=1,
    )
    assert isinstance(effect, hot)

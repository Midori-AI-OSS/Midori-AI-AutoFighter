import sys
import types

pygame_stub = types.ModuleType("pygame")
pygame_stub.image = types.SimpleNamespace(load=lambda *args, **kwargs: object())
sys.modules.setdefault("pygame", pygame_stub)

colorama_stub = types.ModuleType("colorama")


class DummyColor:
    def __getattr__(self, _):
        return ""


colorama_stub.Fore = DummyColor()
colorama_stub.Style = DummyColor()
sys.modules.setdefault("colorama", colorama_stub)

halo_stub = types.ModuleType("halo")


class DummyHalo:
    def __init__(self, *args, **kwargs) -> None:
        ...


halo_stub.Halo = DummyHalo
sys.modules.setdefault("halo", halo_stub)

from damage_over_time import get_dot, dot
from plugins.plugin_loader import PluginLoader


class DummyTarget:
    def __init__(self, hp: int = 100) -> None:
        self.HP = hp


def test_poison_deals_damage_over_time():
    loader = PluginLoader()
    loader.discover("plugins")
    plugin_cls = loader.get_plugins("dot")["poison"]
    target = DummyTarget()
    effect = plugin_cls(damage=10, turns=2)
    starting_hp = target.HP

    assert effect.tick(target, 1) is True
    assert target.HP == starting_hp - 10

    assert effect.tick(target, 1) is False
    assert target.HP == starting_hp - 20


def test_dot_fallback_when_missing(tmp_path):
    effect = get_dot(
        "missing",
        plugin_dir=str(tmp_path),
        name="Fallback",
        damage=1,
        turns=1,
    )
    assert isinstance(effect, dot)

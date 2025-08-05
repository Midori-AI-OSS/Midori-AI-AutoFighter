import importlib

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:  # pragma: no cover - skip if Panda3D missing
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

from autofighter.rooms.boss_room import BossRoom
from autofighter.rooms import boss_patterns
from autofighter.map_generation import load_room_class
from autofighter.stats import Stats


class DummyApp:
    def accept(self, *_args, **_kwargs):
        pass

    def ignore(self, *_args, **_kwargs):
        pass


def test_boss_room_attack_pattern() -> None:
    info = boss_patterns.get_boss_info("demo")
    stats = Stats(hp=100, max_hp=100)
    room = BossRoom(DummyApp(), return_scene_factory=lambda: None, player=stats, boss_name="demo")
    room.attack_button = {"state": None}
    room.status_label = {"text": ""}
    room.player_model = object()
    room.foe_model = object()
    room.show_damage = lambda *a, **k: None
    room.show_attack_effect = lambda *a, **k: None
    room.add_status_icon = lambda *a, **k: None
    room.foe_attack()
    assert stats.hp == 100 - info.attacks[0]
    room.foe_attack()
    assert stats.hp == 100 - info.attacks[0] - info.attacks[1]


def test_map_generation_loads_boss_room() -> None:
    assert load_room_class("battle_boss") is BossRoom
    assert load_room_class("battle_boss_floor") is BossRoom

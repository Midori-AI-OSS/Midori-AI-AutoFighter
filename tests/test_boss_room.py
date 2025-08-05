import importlib

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:  # pragma: no cover - skip if Panda3D missing
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

import random

from autofighter.balance.loop import scale_stats
from autofighter.balance.pressure import apply_pressure
from autofighter.map_generation import load_room_class
from autofighter.rewards import select_rewards
from autofighter.rooms import boss_patterns
from autofighter.rooms.boss_room import BossRoom
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


def test_floor_boss_scales_with_loop_and_pressure() -> None:
    app = DummyApp()
    room = BossRoom(
        app,
        return_scene_factory=lambda: None,
        floor=2,
        room=3,
        loop=2,
        pressure=10,
        floor_boss=True,
    )
    base = Stats(hp=50, max_hp=50, atk=5, defense=3)
    expected = apply_pressure(
        scale_stats(base, 2, 3, 2, floor_boss=True),
        10,
    )
    assert room.foe.hp == expected.hp
    assert room.foe.atk == expected.atk


def test_floor_boss_rewards_scale() -> None:
    rng1 = random.Random(0)
    low = select_rewards(floor_boss=True, loop=1, pressure=0, rng=rng1)
    rng2 = random.Random(0)
    high = select_rewards(floor_boss=True, loop=3, pressure=40, rng=rng2)
    assert high.gold > low.gold
    assert high.tickets > low.tickets

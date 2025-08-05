import importlib

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:  # pragma: no cover - skip if Panda3D missing
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)


from autofighter.battle_room import BattleRoom
from autofighter.stats import Stats


class DummyTaskMgr:
    def doMethodLater(self, *_args, **_kwargs):  # pragma: no cover - no scheduling
        return None

    def remove(self, *_args, **_kwargs) -> None:  # pragma: no cover - cleanup stub
        pass


class DummyApp:
    def __init__(self) -> None:
        self.taskMgr = DummyTaskMgr()

    def accept(self, *_args, **_kwargs):  # pragma: no cover - event wiring stub
        pass

    def ignore(self, *_args, **_kwargs):  # pragma: no cover - event wiring stub
        pass

    def setBackgroundColor(self, *_args, **_kwargs):  # pragma: no cover - visual stub
        pass


def make_room(**kwargs) -> BattleRoom:
    app = DummyApp()
    room = BattleRoom(app, return_scene_factory=lambda: None, **kwargs)
    room.foe = Stats(hp=10, max_hp=10, atk=0, defense=0)
    room.status_label = {"text": ""}
    room.player_model = object()
    room.foe_model = object()
    room.show_damage = lambda *a, **k: None
    room.show_attack_effect = lambda *a, **k: None
    room.add_status_icon = lambda *a, **k: None
    return room


def test_turn_counter_tracks_full_round() -> None:
    room = make_room(player=Stats(hp=10, max_hp=10, atk=0, defense=0))
    room.run_round()
    assert room.turn == 1


def test_overtime_triggers_at_threshold() -> None:
    room = make_room(player=Stats(hp=10, max_hp=10, atk=0, defense=0))
    room.turn = room.overtime_threshold - 1
    room.run_round()
    assert room.overtime

    boss_room = make_room(player=Stats(hp=10, max_hp=10, atk=0, defense=0), floor_boss=True)
    boss_room.turn = boss_room.overtime_threshold - 1
    boss_room.run_round()
    assert boss_room.overtime

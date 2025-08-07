from autofighter.stats import Stats
from autofighter.rest_room import RestRoom


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = type("SM", (), {"switch_to": lambda self, scene: setattr(self, "scene", scene)})()

    def accept(self, *_args, **_kwargs):
        pass

    def ignore(self, *_args, **_kwargs):
        pass


def make_room(items=None):
    app = DummyApp()
    stats = Stats(hp=10, max_hp=10, atk=0, defense=0)
    room = RestRoom(app, stats, return_scene_factory=lambda: None, items=items)
    room.setup()
    return room, stats


def test_heal_restores_hp_and_consumes_use():
    RestRoom.uses_per_floor = {}
    room, stats = make_room()
    stats.hp = 5
    room.heal()
    assert stats.hp == stats.max_hp
    assert RestRoom.uses_per_floor[1] == 1
    assert room.heal_button["state"] == "disabled"
    assert room.trade_button["state"] == "disabled"
    room.teardown()


def test_trade_consumes_stone_and_grants_max_hp():
    RestRoom.uses_per_floor = {}
    room, stats = make_room({"Upgrade Stone": 1})
    room.trade()
    assert stats.max_hp == 15
    assert stats.hp == 15
    assert room.items["Upgrade Stone"] == 0
    assert RestRoom.uses_per_floor[1] == 1
    room.teardown()


def test_should_spawn_respects_minimum():
    RestRoom.min_rests_per_floor = 2
    assert RestRoom.should_spawn(0)
    assert not RestRoom.should_spawn(2)

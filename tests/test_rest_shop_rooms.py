import importlib

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:  # pragma: no cover - skip if Panda3D missing
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

from autofighter.rest_room import RestRoom
from autofighter.shop_room import ShopItem
from autofighter.shop_room import ShopRoom
from autofighter.stats import Stats


class DummyApp:
    scene_manager = type("SM", (), {"switch_to": lambda self, scene: None})()

    def accept(self, *_args, **_kwargs):
        pass

    def ignore(self, *_args, **_kwargs):
        pass


def test_rest_room_heal_uses_limit() -> None:
    RestRoom.uses_per_floor.clear()
    stats = Stats(hp=1, max_hp=5)
    room = RestRoom(DummyApp(), stats, return_scene_factory=lambda: None, floor=1, items={"Upgrade Stone": 1})
    room._animate = lambda _m: None
    room.heal()
    assert stats.hp == 5
    assert RestRoom.uses_per_floor[1] == 1
    assert room._uses_left() == 0


def test_shop_room_buy_disables_button() -> None:
    ShopRoom.spawns_per_floor.clear()
    room = ShopRoom(DummyApp(), return_scene_factory=lambda: None, floor=1)
    button = {"state": "normal"}
    item = ShopItem("Upgrade Stone", 20, 1)
    room.buy(item, button)
    assert room.inventory["Upgrade Stone"] == 1
    assert button["state"] == "disabled"

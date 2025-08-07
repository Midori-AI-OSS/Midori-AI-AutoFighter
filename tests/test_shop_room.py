from __future__ import annotations

import importlib

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:  # pragma: no cover - skip if Panda3D missing
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

import autofighter.save as save

from autofighter.stats import Stats
from autofighter.shop_room import ShopItem
from autofighter.shop_room import ShopRoom


class DummyApp:
    scene_manager = type("SM", (), {"switch_to": lambda self, scene: None})()

    def accept(self, *_args, **_kwargs) -> None:
        pass

    def ignore(self, *_args, **_kwargs) -> None:
        pass


def test_buy_disables_button() -> None:
    ShopRoom.spawns_per_floor.clear()
    room = ShopRoom(DummyApp(), return_scene_factory=lambda: None, floor=1)
    button = {"state": "normal"}
    item = ShopItem("Upgrade Stone", 20, 1)
    room.buy(item, button)
    assert room.inventory["Upgrade Stone"] == 1
    assert button["state"] == "disabled"


def test_reroll_cost_and_refresh() -> None:
    room = ShopRoom(DummyApp(), return_scene_factory=lambda: None, floor=1)
    room.gold = 30

    calls: list[int] = []

    def roll_items() -> None:
        if not calls:
            room.stock = [ShopItem("A", 10, 1)]
        else:
            room.stock = [ShopItem("B", 10, 1)]
        calls.append(1)

    room._roll_items = roll_items  # type: ignore[assignment]
    room._refresh_shop = lambda: roll_items()  # type: ignore[assignment]

    room._refresh_shop()
    assert room.stock[0].name == "A"
    room.reroll()
    assert room.gold == 20
    assert room.stock[0].name == "B"


def test_should_spawn_respects_minimum() -> None:
    ShopRoom.spawns_per_floor = {}
    ShopRoom.min_shops_per_floor = 2
    assert ShopRoom.should_spawn(1)
    ShopRoom.record_spawn(1)
    assert ShopRoom.should_spawn(1)
    ShopRoom.record_spawn(1)
    assert not ShopRoom.should_spawn(1)


def test_exit_persists_inventory(monkeypatch) -> None:
    store: dict[str, tuple[str, str, str, str, Stats, dict[str, int]]] = {}

    def fake_save_player(body, hair, hair_color, accessory, stats, inventory, **_kwargs):
        store["data"] = (body, hair, hair_color, accessory, stats, inventory)

    def fake_load_player(*_args, **_kwargs):
        return store.get("data")

    monkeypatch.setattr(save, "save_player", fake_save_player)
    monkeypatch.setattr(save, "load_player", fake_load_player)
    monkeypatch.setattr("autofighter.shop_room.save_player", fake_save_player)
    monkeypatch.setattr("autofighter.shop_room.load_player", fake_load_player)

    store["data"] = ("Athletic", "Short", "Black", "None", Stats(hp=5, max_hp=5, gold=100), {})

    room = ShopRoom(DummyApp(), return_scene_factory=lambda: None, floor=1)
    button = {"state": "normal"}
    item = ShopItem("Upgrade Stone", 20, 1)
    room.buy(item, button)
    room.exit()

    loaded = save.load_player()
    assert loaded is not None
    _, _, _, _, stats, inventory = loaded
    assert inventory["Upgrade Stone"] == 1
    assert stats.gold == 80

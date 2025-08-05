from __future__ import annotations

from autofighter.gacha.crafting_menu import CraftingMenu


class SceneManagerStub:
    def __init__(self) -> None:
        self.popped = False

    def pop_overlay(self) -> None:
        self.popped = True


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = SceneManagerStub()
        self.events: dict[str, object] = {}

    def accept(self, name: str, func) -> None:
        self.events[name] = func

    def ignore(self, name: str) -> None:
        self.events.pop(name, None)


def test_crafting_menu_upgrades_items() -> None:
    items = {1: 125, 2: 0, 3: 0, 4: 0}
    app = DummyApp()
    menu = CraftingMenu(app, items)
    menu.setup()
    menu.craft()
    assert items[1] == 0
    assert items[2] == 1
    assert "1\u2605:0" in menu.craft_button["text"]
    assert "2\u2605:1" in menu.craft_button["text"]
    menu.teardown()


def test_crafting_menu_back_pops_overlay() -> None:
    app = DummyApp()
    menu = CraftingMenu(app, {})
    menu.setup()
    menu.back()
    assert app.scene_manager.popped is True
    menu.teardown()

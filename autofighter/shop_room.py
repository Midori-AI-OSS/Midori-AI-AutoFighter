from __future__ import annotations

import random

from dataclasses import dataclass

from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from direct.showbase.ShowBase import ShowBase

from autofighter.gui import set_widget_pos
from autofighter.scene import Scene


@dataclass
class ShopItem:
    """Item sold in the shop."""

    name: str
    price: int
    star: int


class ShopRoom(Scene):
    """Scene selling upgrade items and cards with reroll option."""

    reroll_cost: int = 10
    min_shops_per_floor: int = 2
    spawns_per_floor: dict[int, int] = {}

    def __init__(
        self,
        app: ShowBase,
        return_scene_factory,
        *,
        floor: int = 1,
        inventory: dict[str, int] | None = None,
    ) -> None:
        self.app = app
        self.return_scene_factory = return_scene_factory
        self.gold = 100
        self.floor = floor
        self.inventory = inventory or {}
        self.stock: list[ShopItem] = []
        self.widgets: list[DirectButton | DirectLabel] = []
        self.info_label: DirectLabel | None = None
        ShopRoom.record_spawn(self.floor)

    def setup(self) -> None:
        self.info_label = DirectLabel(
            text=self._info_text(),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.info_label, (0, 0, 0.7))
        self.widgets.append(self.info_label)
        self._refresh_shop()
        self.app.accept("escape", self.exit)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.app.ignore("escape")

    def buy(self, item: ShopItem, button: DirectButton) -> None:
        if self.gold < item.price or button["state"] == "disabled":
            return
        self.gold -= item.price
        self.inventory[item.name] = self.inventory.get(item.name, 0) + 1
        button["state"] = "disabled"
        self._update_info()

    def reroll(self) -> None:
        if self.gold < ShopRoom.reroll_cost:
            return
        self.gold -= ShopRoom.reroll_cost
        self._refresh_shop()

    def _refresh_shop(self) -> None:
        for widget in self.widgets[1:]:
            widget.destroy()
        self.widgets = self.widgets[:1]
        self._roll_items()
        for i, item in enumerate(self.stock):
            star_text = "\u2605" * item.star
            button = DirectButton(
                text=f"{item.name} {star_text} ({item.price})",
                command=lambda: None,
                frameColor=(0, 0, 0, 0.5),
                text_fg=(1, 1, 1, 1),
            )
            set_widget_pos(button, (0, 0, 0.2 - i * 0.3))
            button["command"] = lambda it=item, btn=button: self.buy(it, btn)
            self.widgets.append(button)
        reroll_button = DirectButton(
            text=f"Reroll ({ShopRoom.reroll_cost})",
            command=self.reroll,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(reroll_button, (-0.3, 0, -0.7))
        leave_button = DirectButton(
            text="Leave",
            command=self.exit,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(leave_button, (0.3, 0, -0.7))
        self.widgets.extend([reroll_button, leave_button])
        self._update_info()

    def _roll_items(self) -> None:
        pool = [
            ShopItem("Upgrade Stone", 20, 1),
            ShopItem("Power Card", 15, 1),
            ShopItem("Defense Card", 15, 1),
            ShopItem("Speed Upgrade", 25, 2),
            ShopItem("Health Card", 10, 1),
        ]
        max_star = min(1 + self.floor // 5, 5)
        candidates = [item for item in pool if item.star <= max_star]
        self.stock = random.sample(candidates, 3)

    @classmethod
    def record_spawn(cls, floor: int) -> None:
        cls.spawns_per_floor[floor] = cls.spawns_per_floor.get(floor, 0) + 1

    @classmethod
    def should_spawn(cls, floor: int) -> bool:
        """Return True if another shop should spawn on this floor."""

        return cls.spawns_per_floor.get(floor, 0) < cls.min_shops_per_floor

    def _update_info(self) -> None:
        assert self.info_label is not None
        self.info_label["text"] = self._info_text()

    def _info_text(self) -> str:
        return f"Gold: {self.gold}"

    def exit(self) -> None:
        self.app.scene_manager.switch_to(self.return_scene_factory())

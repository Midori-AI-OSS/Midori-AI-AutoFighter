from __future__ import annotations

from typing import Any
from typing import Callable

from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectOptionMenu
from direct.gui.DirectGui import DirectSlider
from direct.showbase.ShowBase import ShowBase

from autofighter.save import save_player
from autofighter.scene import Scene
from autofighter.stats import Stats

DAMAGE_TYPES = [
    "generic",
    "light",
    "dark",
    "wind",
    "lightning",
    "fire",
    "ice",
]


class PlayerCreator(Scene):
    def __init__(
        self,
        app: ShowBase,
        return_scene_factory: Callable[[], Scene] | None = None,
        extras: dict[str, int] | None = None,
        inventory: dict[str, int] | None = None,
    ) -> None:
        self.app = app
        self.return_scene_factory = return_scene_factory
        self.extras = extras or {}
        self.inventory = {t: (inventory or {}).get(t, 0) for t in DAMAGE_TYPES}
        bonus = min(self.inventory[t] // 100 for t in DAMAGE_TYPES) if DAMAGE_TYPES else 0
        if bonus:
            for t in DAMAGE_TYPES:
                self.inventory[t] -= bonus * 100
        self.body_options = ["Athletic", "Slim", "Heavy"]
        self.hair_options = ["Short", "Long", "Ponytail"]
        self.color_options = ["Black", "Blonde", "Red"]
        self.accessory_options = ["None", "Hat", "Glasses"]
        self.body_choice = self.body_options[0]
        self.hair_choice = self.hair_options[0]
        self.hair_color_choice = self.color_options[0]
        self.accessory_choice = self.accessory_options[0]
        self.total_points = 100 + bonus
        self.sliders: dict[str, DirectSlider] = {}
        self.widgets: list[Any] = []
        self.remaining_label: DirectLabel | None = None
        self.confirm_button: DirectButton | None = None

    def setup(self) -> None:
        body = DirectOptionMenu(
            text="Body",
            items=self.body_options,
            initialitem=0,
            pos=(0, 0, 0.8),
            command=self.set_body,
        )
        hair = DirectOptionMenu(
            text="Hair",
            items=self.hair_options,
            initialitem=0,
            pos=(0, 0, 0.6),
            command=self.set_hair,
        )
        color = DirectOptionMenu(
            text="Color",
            items=self.color_options,
            initialitem=0,
            pos=(0, 0, 0.4),
            command=self.set_color,
        )
        accessory = DirectOptionMenu(
            text="Accessory",
            items=self.accessory_options,
            initialitem=0,
            pos=(0, 0, 0.2),
            command=self.set_accessory,
        )
        hp_slider = DirectSlider(
            range=(0, self.total_points),
            value=0,
            pos=(0, 0, 0.0),
            scale=0.5,
            command=self.on_slider_change,
            extraArgs=["hp"],
        )
        atk_slider = DirectSlider(
            range=(0, self.total_points),
            value=0,
            pos=(0, 0, -0.2),
            scale=0.5,
            command=self.on_slider_change,
            extraArgs=["atk"],
        )
        def_slider = DirectSlider(
            range=(0, self.total_points),
            value=0,
            pos=(0, 0, -0.4),
            scale=0.5,
            command=self.on_slider_change,
            extraArgs=["defense"],
        )
        self.sliders = {
            "hp": hp_slider,
            "atk": atk_slider,
            "defense": def_slider,
        }
        self.remaining_label = DirectLabel(text=f"Points left: {self.total_points}", pos=(0, 0, -0.5))
        confirm = DirectButton(text="Confirm", pos=(0, 0, -0.7), command=self.confirm, state="disabled")
        cancel = DirectButton(text="Cancel", pos=(0, 0, -0.9), command=self.cancel)
        self.confirm_button = confirm
        self.widgets = [
            body,
            hair,
            color,
            accessory,
            hp_slider,
            atk_slider,
            def_slider,
            self.remaining_label,
            confirm,
            cancel,
        ]

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()

    def set_body(self, choice: str) -> None:
        self.body_choice = choice

    def set_hair(self, choice: str) -> None:
        self.hair_choice = choice

    def set_color(self, choice: str) -> None:
        self.hair_color_choice = choice

    def set_accessory(self, choice: str) -> None:
        self.accessory_choice = choice

    def on_slider_change(self, stat: str) -> None:
        total = sum(int(s["value"]) for s in self.sliders.values())
        if total > self.total_points:
            excess = total - self.total_points
            slider = self.sliders[stat]
            slider["value"] = max(0, slider["value"] - excess)
        self.update_remaining()

    def update_remaining(self) -> None:
        total = sum(int(s["value"]) for s in self.sliders.values())
        remaining = self.total_points - total
        if self.remaining_label:
            self.remaining_label["text"] = f"Points left: {remaining}"
        if self.confirm_button:
            self.confirm_button["state"] = "normal" if remaining == 0 else "disabled"

    def confirm(self) -> None:
        base = {k: int(s["value"]) for k, s in self.sliders.items()}
        stats = Stats(
            hp=base["hp"] + self.extras.get("hp", 0),
            max_hp=base["hp"] + self.extras.get("hp", 0),
            atk=base["atk"] + self.extras.get("atk", 0),
            defense=base["defense"] + self.extras.get("defense", 0),
        )
        save_player(
            self.body_choice,
            self.hair_choice,
            self.hair_color_choice,
            self.accessory_choice,
            stats,
        )
        if self.return_scene_factory:
            self.app.scene_manager.switch_to(self.return_scene_factory())

    def cancel(self) -> None:
        if self.return_scene_factory:
            self.app.scene_manager.switch_to(self.return_scene_factory())

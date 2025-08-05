from __future__ import annotations

from typing import Any
from typing import Callable

try:
    from direct.gui.DirectGui import DirectButton
    from direct.gui.DirectGui import DirectLabel
    from direct.gui.DirectGui import DirectOptionMenu
    from direct.gui.DirectGui import DirectSlider
    from direct.showbase.ShowBase import ShowBase
except Exception:  # pragma: no cover - fallback for headless tests
    class DirectButton:  # type: ignore[dead-code]
        pass

    class DirectLabel:  # type: ignore[dead-code]
        pass

    class DirectOptionMenu:  # type: ignore[dead-code]
        pass

    class DirectSlider:  # type: ignore[dead-code]
        def __getitem__(self, _key: str) -> float:
            return 0.0

        def __setitem__(self, _key: str, _value: float) -> None:
            pass

    class ShowBase:  # type: ignore[dead-code]
        pass

from autofighter.gui import WIDGET_SCALE
from autofighter.gui import set_widget_pos
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

BASE_STATS = {
    "hp": 100,
    "atk": 10,
    "defense": 10,
}


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
        self.bonus = min(self.inventory[t] // 100 for t in DAMAGE_TYPES) if DAMAGE_TYPES else 0
        self.body_options = ["Athletic", "Slim", "Heavy"]
        self.hair_options = ["Short", "Long", "Ponytail"]
        self.color_options = ["Black", "Blonde", "Red"]
        self.accessory_options = ["None", "Hat", "Glasses"]
        self.body_choice = self.body_options[0]
        self.hair_choice = self.hair_options[0]
        self.hair_color_choice = self.color_options[0]
        self.accessory_choice = self.accessory_options[0]
        self.total_points = 100 + self.bonus
        self.sliders: dict[str, DirectSlider] = {}
        self.widgets: list[Any] = []
        self.remaining_label: DirectLabel | None = None
        self.confirm_button: DirectButton | None = None

    def setup(self) -> None:
        body = DirectOptionMenu(
            text="Body",
            items=self.body_options,
            initialitem=0,
            command=self.set_body,
            scale=WIDGET_SCALE,
        )
        set_widget_pos(body, (0, 0, 0.8))
        hair = DirectOptionMenu(
            text="Hair",
            items=self.hair_options,
            initialitem=0,
            command=self.set_hair,
            scale=WIDGET_SCALE,
        )
        set_widget_pos(hair, (0, 0, 0.6))
        color = DirectOptionMenu(
            text="Color",
            items=self.color_options,
            initialitem=0,
            command=self.set_color,
            scale=WIDGET_SCALE,
        )
        set_widget_pos(color, (0, 0, 0.4))
        accessory = DirectOptionMenu(
            text="Accessory",
            items=self.accessory_options,
            initialitem=0,
            command=self.set_accessory,
            scale=WIDGET_SCALE,
        )
        set_widget_pos(accessory, (0, 0, 0.2))
        hp_slider = DirectSlider(
            range=(0, self.total_points),
            value=0,
            scale=WIDGET_SCALE * 5,
            command=self.on_slider_change,
            extraArgs=["hp"],
        )
        set_widget_pos(hp_slider, (0, 0, 0.0))
        atk_slider = DirectSlider(
            range=(0, self.total_points),
            value=0,
            scale=WIDGET_SCALE * 5,
            command=self.on_slider_change,
            extraArgs=["atk"],
        )
        set_widget_pos(atk_slider, (0, 0, -0.2))
        def_slider = DirectSlider(
            range=(0, self.total_points),
            value=0,
            scale=WIDGET_SCALE * 5,
            command=self.on_slider_change,
            extraArgs=["defense"],
        )
        set_widget_pos(def_slider, (0, 0, -0.4))
        self.sliders = {
            "hp": hp_slider,
            "atk": atk_slider,
            "defense": def_slider,
        }
        self.remaining_label = DirectLabel(text=f"Points left: {self.total_points}", scale=WIDGET_SCALE)
        set_widget_pos(self.remaining_label, (0, 0, -0.5))
        confirm = DirectButton(text="Confirm", command=self.confirm, state="normal", scale=WIDGET_SCALE)
        set_widget_pos(confirm, (0, 0, -0.7))
        cancel = DirectButton(text="Cancel", command=self.cancel, scale=WIDGET_SCALE)
        set_widget_pos(cancel, (0, 0, -0.9))
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
            self.confirm_button["state"] = "normal"

    def confirm(self) -> None:
        raw_points = {k: int(s["value"]) for k, s in self.sliders.items()}
        spent = sum(raw_points.values())
        bonus_used = min(self.bonus, max(0, spent - 100))
        for t in DAMAGE_TYPES:
            self.inventory[t] -= bonus_used * 100
        points = {k: raw_points[k] + self.extras.get(k, 0) for k in raw_points}
        stats = Stats(
            hp=int(BASE_STATS["hp"] * (1 + points["hp"] / 100)),
            max_hp=int(BASE_STATS["hp"] * (1 + points["hp"] / 100)),
            atk=int(BASE_STATS["atk"] * (1 + points["atk"] / 100)),
            defense=int(BASE_STATS["defense"] * (1 + points["defense"] / 100)),
        )
        save_player(
            self.body_choice,
            self.hair_choice,
            self.hair_color_choice,
            self.accessory_choice,
            stats,
            self.inventory,
        )
        if self.return_scene_factory:
            self.app.scene_manager.switch_to(self.return_scene_factory())

    def cancel(self) -> None:
        if self.return_scene_factory:
            self.app.scene_manager.switch_to(self.return_scene_factory())

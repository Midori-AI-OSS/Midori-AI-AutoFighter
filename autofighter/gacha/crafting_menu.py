from __future__ import annotations

from typing import Dict

try:
    from direct.gui.DirectGui import DirectButton
    from direct.showbase.ShowBase import ShowBase
except Exception:  # pragma: no cover - headless fallback
    class _Widget:
        def __init__(self, **kwargs: object) -> None:
            self.options = dict(kwargs)

        def __getitem__(self, key: str) -> object:
            return self.options.get(key)

        def __setitem__(self, key: str, value: object) -> None:
            self.options[key] = value

        def destroy(self) -> None:  # noqa: D401 - match Panda3D API
            """Pretend to remove the widget."""

    class DirectButton(_Widget):  # type: ignore[dead-code]
        pass

    class ShowBase:  # type: ignore[dead-code]
        pass

from autofighter.gui import TEXT_COLOR
from autofighter.gui import FRAME_COLOR
from autofighter.gui import set_widget_pos
from autofighter.gui import get_widget_scale
from autofighter.scene import Scene
from .crafting import craft_upgrades


class CraftingMenu(Scene):
    """Menu for converting upgrade items to higher stars."""

    BUTTON_SPACING = 0.25

    def __init__(self, app: ShowBase, items: Dict[int, int]) -> None:
        self.app = app
        self.items = items
        self.buttons: list[DirectButton] = []
        self._craft_button: DirectButton | None = None
        self._back_button: DirectButton | None = None

    def setup(self) -> None:
        self._craft_button = DirectButton(
            text=self._button_text(),
            frameColor=FRAME_COLOR,
            text_fg=TEXT_COLOR,
            command=self.craft,
            scale=get_widget_scale(),
        )
        self._back_button = DirectButton(
            text="Back",
            frameColor=FRAME_COLOR,
            text_fg=TEXT_COLOR,
            command=self.back,
            scale=get_widget_scale(),
        )
        self.buttons = [self._craft_button, self._back_button]
        top = self.BUTTON_SPACING * (len(self.buttons) - 1) / 2
        for i, button in enumerate(self.buttons):
            set_widget_pos(button, (0, 0, top - i * self.BUTTON_SPACING))
        self.app.accept("escape", self.back)

    def teardown(self) -> None:
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        self.app.ignore("escape")

    def _button_text(self) -> str:
        counts = " ".join(
            f"{star}\u2605:{self.items.get(star, 0)}" for star in (1, 2, 3, 4)
        )
        return f"Craft {counts}"

    def craft(self) -> None:
        craft_upgrades(self.items)
        if self._craft_button:
            self._craft_button["text"] = self._button_text()

    def back(self) -> None:
        self.app.scene_manager.pop_overlay()

    @property
    def craft_button(self) -> DirectButton:
        assert self._craft_button is not None
        return self._craft_button

    @property
    def back_button(self) -> DirectButton:
        assert self._back_button is not None
        return self._back_button

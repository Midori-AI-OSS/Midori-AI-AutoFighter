from __future__ import annotations

import random

from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectEntry
from direct.gui.DirectGui import DirectLabel
from direct.showbase.ShowBase import ShowBase

from autofighter.events import Event
from autofighter.gui import set_widget_pos
from autofighter.scene import Scene
from autofighter.stats import Stats

class EventRoom(Scene):
    """Scene that plays one text event with choices."""

    consumes_room: bool = False

    def __init__(
        self,
        app: ShowBase,
        stats: Stats,
        return_scene_factory,
        *,
        items: dict[str, int] | None = None,
        event: Event | None = None,
    ) -> None:
        self.app = app
        self.stats = stats
        self.return_scene_factory = return_scene_factory
        self.items = items or {}
        if event is not None:
            self.event = event
        else:
            events = app.plugin_loader.get_plugins("event")
            builder = random.choice(list(events.values()))
            self.event = builder.build()
        self.widgets: list[DirectButton | DirectEntry | DirectLabel] = []
        self.result_label: DirectLabel | None = None

    def setup(self) -> None:
        prompt = DirectLabel(
            text=self.event.prompt,
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(prompt, (0, 0, 0.7))
        self.widgets.append(prompt)
        for i, option in enumerate(self.event.options):
            button = DirectButton(
                text=option.text,
                command=lambda idx=i: self.choose(idx),
                frameColor=(0, 0, 0, 0.5),
                text_fg=(1, 1, 1, 1),
            )
            set_widget_pos(button, (0, 0, 0.3 - i * 0.2))
            self.widgets.append(button)
        self.result_label = DirectLabel(
            text="",
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.result_label, (0, 0, -0.1))
        self.widgets.append(self.result_label)
        leave = DirectButton(
            text="Leave",
            command=self.exit,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(leave, (0, 0, -0.8))
        self.widgets.append(leave)
        self.app.accept("escape", self.exit)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.app.ignore("escape")

    def choose(self, index: int) -> None:
        if self.result_label is None:
            return
        message = self.event.resolve(index, self.stats, self.items)
        self.result_label["text"] = message
        for widget in self.widgets:
            if isinstance(widget, DirectButton) and widget["text"] != "Leave":
                widget["state"] = "disabled"

    def exit(self) -> None:
        self.app.scene_manager.switch_to(self.return_scene_factory())

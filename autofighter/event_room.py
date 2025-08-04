from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectEntry
from direct.showbase.ShowBase import ShowBase

from autofighter.scene import Scene
from autofighter.stats import Stats


@dataclass
class EventOption:
    """A selectable outcome for an event."""

    text: str
    effect: Callable[[Stats, dict[str, int], random.Random], str]


@dataclass
class Event:
    """Text prompt with deterministic outcomes."""

    prompt: str
    options: list[EventOption]
    seed: int = 0

    def resolve(self, choice: int, stats: Stats, items: dict[str, int]) -> str:
        rng = random.Random(self.seed)
        return self.options[choice].effect(stats, items, rng)


# Sample events -----------------------------------------------------------------

def _fountain_effect(stats: Stats, _items: dict[str, int], rng: random.Random) -> str:
    heal = rng.randint(5, 10)
    stats.apply_healing(heal)
    return f"You feel restored: +{heal} HP"


def _chest_effect(stats: Stats, items: dict[str, int], rng: random.Random) -> str:
    if rng.random() < 0.5:
        items["Upgrade Stone"] = items.get("Upgrade Stone", 0) + 1
        return "Inside you find an Upgrade Stone!"
    damage = rng.randint(1, 5)
    stats.apply_damage(damage)
    return f"A trap! You take {damage} damage."


SAMPLE_EVENTS = [
    Event(
        "A shimmering fountain beckons. Drink?",
        [
            EventOption("Drink", _fountain_effect),
            EventOption("Leave", lambda *_: "You walk away."),
        ],
        seed=1,
    ),
    Event(
        "A dusty chest sits alone. Open it?",
        [
            EventOption("Open", _chest_effect),
            EventOption("Ignore", lambda *_: "You move on."),
        ],
        seed=2,
    ),
]


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
        self.event = event or random.choice(SAMPLE_EVENTS)
        self.widgets: list[DirectButton | DirectEntry | DirectLabel] = []
        self.result_label: DirectLabel | None = None

    def setup(self) -> None:
        prompt = DirectLabel(
            text=self.event.prompt,
            pos=(0, 0, 0.7),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        self.widgets.append(prompt)
        for i, option in enumerate(self.event.options):
            button = DirectButton(
                text=option.text,
                command=lambda idx=i: self.choose(idx),
                pos=(0, 0, 0.3 - i * 0.2),
                frameColor=(0, 0, 0, 0.5),
                text_fg=(1, 1, 1, 1),
            )
            self.widgets.append(button)
        self.result_label = DirectLabel(
            text="",
            pos=(0, 0, -0.1),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        self.widgets.append(self.result_label)
        leave = DirectButton(
            text="Leave",
            command=self.exit,
            pos=(0, 0, -0.8),
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
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


class ChatRoom(Scene):
    """Scene allowing one-message chats with LLM characters."""

    chats_per_floor: dict[int, int] = {}
    max_chats_per_floor: int = 6

    def __init__(
        self,
        app: ShowBase,
        return_scene_factory,
        *,
        floor: int = 1,
        character: str = "Guide",
    ) -> None:
        self.app = app
        self.return_scene_factory = return_scene_factory
        self.floor = floor
        self.character = character
        self.entry: DirectEntry | None = None
        self.response_label: DirectLabel | None = None
        self.widgets: list[DirectButton | DirectEntry | DirectLabel] = []

    def setup(self) -> None:
        prompt = DirectLabel(
            text=f"Chat with {self.character}",
            pos=(0, 0, 0.7),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        self.entry = DirectEntry(
            initialText="",
            numLines=1,
            pos=(-0.5, 0, 0.3),
            scale=0.05,
        )
        send = DirectButton(
            text="Send",
            command=self.send,
            pos=(0.6, 0, 0.3),
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        self.response_label = DirectLabel(
            text="",
            pos=(0, 0, -0.1),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        leave = DirectButton(
            text="Leave",
            command=self.exit,
            pos=(0, 0, -0.8),
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        self.widgets = [prompt, self.entry, send, self.response_label, leave]
        if self._chats_left() <= 0:
            if self.entry is not None:
                self.entry["state"] = "disabled"
            send["state"] = "disabled"
            self.response_label["text"] = "No chats left this floor"
        self.app.accept("escape", self.exit)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.app.ignore("escape")

    def send(self) -> None:
        if self.entry is None or self.response_label is None:
            return
        if self._chats_left() <= 0:
            return
        message = self.entry.get()
        self.response_label["text"] = f"{self.character} replies: {message}"
        self.entry["state"] = "disabled"
        self.widgets[2]["state"] = "disabled"  # send button
        self._record_chat()

    def _chats_left(self) -> int:
        used = ChatRoom.chats_per_floor.get(self.floor, 0)
        return ChatRoom.max_chats_per_floor - used

    def _record_chat(self) -> None:
        ChatRoom.chats_per_floor[self.floor] = ChatRoom.chats_per_floor.get(self.floor, 0) + 1

    @staticmethod
    def should_spawn(chats_seen: int) -> bool:
        return chats_seen < ChatRoom.max_chats_per_floor

    def exit(self) -> None:
        self.app.scene_manager.switch_to(self.return_scene_factory())

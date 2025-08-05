from __future__ import annotations

from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectEntry
from direct.gui.DirectGui import DirectLabel
from direct.showbase.ShowBase import ShowBase

from autofighter.gui import set_widget_pos
from autofighter.scene import Scene
from autofighter.chat.llm_client import LLMClient
from autofighter.chat.llm_client import get_client


class ChatRoom(Scene):
    """Scene allowing one-message chats with LLM characters."""

    consumes_room: bool = False
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
        self.client = get_client() if LLMClient.available() else None

    def setup(self) -> None:
        prompt = DirectLabel(
            text=f"Chat with {self.character}",
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(prompt, (0, 0, 0.7))
        self.entry = DirectEntry(initialText="", numLines=1, scale=0.05)
        set_widget_pos(self.entry, (-0.5, 0, 0.3))
        send = DirectButton(
            text="Send",
            command=self.send,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(send, (0.6, 0, 0.3))
        self.response_label = DirectLabel(
            text="",
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.response_label, (0, 0, -0.1))
        skip = DirectButton(
            text="Skip",
            command=self.skip,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(skip, (0, 0, -0.8))
        self.widgets = [prompt, self.entry, send, self.response_label, skip]
        if self.client is None or self._chats_left() <= 0:
            if self.entry is not None:
                self.entry["state"] = "disabled"
            send["state"] = "disabled"
            if self.response_label is not None:
                self.response_label["text"] = "No chats available"
        self.app.accept("escape", self.skip)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.app.ignore("escape")

    def send(self) -> None:
        if (
            self.entry is None
            or self.response_label is None
            or self.client is None
            or self._chats_left() <= 0
        ):
            return
        message = self.entry.get()
        reply = self.client.ask(self.character, message)
        self.response_label["text"] = reply
        self.entry["state"] = "disabled"
        self.widgets[2]["state"] = "disabled"  # send button
        self._record_chat()

    def skip(self) -> None:
        self.app.scene_manager.switch_to(self.return_scene_factory())

    def _chats_left(self) -> int:
        used = ChatRoom.chats_per_floor.get(self.floor, 0)
        return ChatRoom.max_chats_per_floor - used

    def _record_chat(self) -> None:
        ChatRoom.chats_per_floor[self.floor] = ChatRoom.chats_per_floor.get(
            self.floor, 0
        ) + 1

    @staticmethod
    def should_spawn(chats_seen: int) -> bool:
        return LLMClient.available() and chats_seen < ChatRoom.max_chats_per_floor

    def exit(self) -> None:
        self.skip()


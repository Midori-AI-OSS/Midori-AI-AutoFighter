import importlib
import sys

from pathlib import Path

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:  # pragma: no cover - Panda3D missing
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

sys.path.append(str(Path(__file__).resolve().parents[1]))

from autofighter.chat import llm_client
from autofighter.rooms.chat_room import ChatRoom


def _dummy_app() -> object:
    switcher = type("SM", (), {"switch_to": lambda self, scene: None})()
    return type("A", (), {"scene_manager": switcher})()


def test_should_spawn_checks_deps(monkeypatch) -> None:
    monkeypatch.setattr(
        llm_client.LLMClient, "available", staticmethod(lambda: False)
    )
    assert not ChatRoom.should_spawn(0)
    monkeypatch.setattr(
        llm_client.LLMClient, "available", staticmethod(lambda: True)
    )
    assert ChatRoom.should_spawn(0)


def test_send_records_chat(monkeypatch) -> None:
    ChatRoom.chats_per_floor.clear()
    dummy_client = type("C", (), {"ask": lambda self, c, m: "hi"})()
    monkeypatch.setattr(
        llm_client.LLMClient, "available", staticmethod(lambda: True)
    )
    monkeypatch.setattr(llm_client, "get_client", lambda *_, **__: dummy_client)
    app = _dummy_app()
    room = ChatRoom(app, return_scene_factory=lambda: None, floor=1)
    entry = type("E", (), {"get": lambda self: "hello", "__setitem__": lambda self, k, v: None})()
    label_store = {"text": ""}
    response_label = type(
        "L", (), {"__setitem__": lambda self, k, v: label_store.__setitem__(k, v)}
    )()
    send_button = type("B", (), {"__setitem__": lambda self, k, v: None})()
    room.entry = entry
    room.response_label = response_label
    room.widgets = [None, entry, send_button, response_label, None]
    room.client = llm_client.get_client()
    room.send()
    assert ChatRoom.chats_per_floor[1] == 1
    assert label_store["text"] == "hi"


def test_skip_does_not_count() -> None:
    ChatRoom.chats_per_floor.clear()
    app = _dummy_app()
    room = ChatRoom(app, return_scene_factory=lambda: None, floor=1)
    room.skip()
    assert ChatRoom.chats_per_floor.get(1) is None


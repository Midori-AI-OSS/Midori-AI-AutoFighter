from types import SimpleNamespace

import pytest

try:
    from panda3d.core import loadPrcFileData
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    pytest.skip("panda3d not installed", allow_module_level=True)

from main import AutoFighterApp


def _make_app() -> AutoFighterApp:
    loadPrcFileData("", "window-type none")
    return AutoFighterApp()


def test_window_close_triggers_exit(monkeypatch) -> None:
    app = _make_app()
    exit_called = False
    orig_exit = app.userExit

    def fake_exit() -> None:
        nonlocal exit_called
        exit_called = True
        orig_exit()

    monkeypatch.setattr(app, "userExit", fake_exit)
    window = SimpleNamespace(is_closed=lambda: True)
    app.on_window_event(window)
    assert exit_called


def test_window_event_ignored(monkeypatch) -> None:
    app = _make_app()
    exit_called = False
    orig_exit = app.userExit

    def fake_exit() -> None:
        nonlocal exit_called
        exit_called = True

    monkeypatch.setattr(app, "userExit", fake_exit)
    window = SimpleNamespace(is_closed=lambda: False)
    app.on_window_event(window)
    app.on_window_event(None)
    assert not exit_called
    orig_exit()


def test_pause_and_resume_toggle_state() -> None:
    app = _make_app()
    try:
        assert not app.paused
        app.pause_game()
        assert app.paused
        app.resume_game()
        assert not app.paused
    finally:
        app.userExit()

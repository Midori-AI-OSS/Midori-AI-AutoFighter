from pathlib import Path

import pytest

import autofighter.save as save
import autofighter.audio as audio

pytest.importorskip("game.ui.options")
from game.ui.options import OptionsMenu


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = object()
        self.pause_on_stats = True
        self.stat_refresh_rate = 5
        self.events: dict[str, object] = {}

    def accept(self, name: str, func) -> None:
        self.events[name] = func

    def ignore(self, name: str) -> None:
        self.events.pop(name, None)

    def userExit(self) -> None:  # noqa: N802 - match ShowBase
        pass


class DummyAssets:
    def load(self, *_: object) -> object:  # pragma: no cover - simple stub
        return object()


def test_options_menu_slider_behavior(tmp_path: Path) -> None:
    save.SETTINGS_PATH = tmp_path / "settings.json"
    audio._global_audio = audio.AudioManager(DummyAssets())

    app = DummyApp()
    menu = OptionsMenu(app)
    menu.setup()

    menu.index = 0  # sfx slider
    start = audio.get_audio().sfx_volume
    menu.increase()
    assert audio.get_audio().sfx_volume > start
    menu.decrease()
    assert audio.get_audio().sfx_volume == start

    menu.index = menu.widgets.index(menu.pause_button)
    state = app.pause_on_stats
    menu.activate()
    assert app.pause_on_stats is not state

    menu.teardown()
    audio._global_audio = None


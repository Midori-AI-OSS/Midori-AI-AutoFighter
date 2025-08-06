from __future__ import annotations

from pathlib import Path

import autofighter.save as save
import autofighter.audio as audio

from autofighter.menu import OptionsMenu


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
    def load(self, *_: object) -> object:
        return object()


def test_options_persist(tmp_path: Path) -> None:
    save.SETTINGS_PATH = tmp_path / "settings.json"
    audio._global_audio = audio.AudioManager(DummyAssets())

    app = DummyApp()
    menu = OptionsMenu(app)
    menu.setup()

    menu.sfx_slider["value"] = 0.7
    menu.update_sfx()
    menu.music_slider["value"] = 0.3
    menu.update_music()
    menu.refresh_slider["value"] = 7
    menu.update_refresh()
    menu.pause_button.setIndicatorValue(False)
    menu.toggle_pause()

    settings = save.load_settings()
    assert settings["sfx_volume"] == 0.7
    assert settings["music_volume"] == 0.3
    assert settings["stat_refresh_rate"] == 7
    assert settings["pause_on_stats"] is False

    menu.teardown()
    audio._global_audio = None

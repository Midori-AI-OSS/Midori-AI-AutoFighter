from __future__ import annotations

from pathlib import Path

from autofighter.menu import LoadRunMenu
from autofighter.menu import MainMenu
from autofighter.menu import OptionsMenu


class DummyAudio:
    def __init__(self) -> None:
        self.volume = 0.0

    def setVolume(self, value: float) -> None:  # noqa: N802 - Panda3D style
        self.volume = value


class DummyApp:
    def __init__(self) -> None:
        self.sfxManagerList = [DummyAudio(), DummyAudio()]
        self.musicManager = DummyAudio()
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

def test_load_run_menu_lists_runs(tmp_path: Path) -> None:
    (tmp_path / "run1.json").write_text("{}")
    (tmp_path / "run2.json").write_text("{}")
    app = DummyApp()
    menu = LoadRunMenu(app)
    LoadRunMenu.RUNS_DIR = tmp_path
    paths = menu.available_runs()
    assert [p.name for p in paths] == ["run1.json", "run2.json"]


def test_options_menu_updates_audio() -> None:
    app = DummyApp()
    menu = OptionsMenu(app)
    menu.setup()
    menu.sfx_slider["value"] = 0.7
    menu.music_slider["value"] = 0.3
    menu.update_sfx()
    menu.update_music()
    assert app.sfxManagerList[0].volume == 0.7
    assert app.sfxManagerList[1].volume == 0.7
    assert app.musicManager.volume == 0.3
    menu.teardown()


def test_options_menu_updates_refresh_rate() -> None:
    app = DummyApp()
    menu = OptionsMenu(app)
    menu.setup()
    menu.refresh_slider["value"] = 7
    menu.update_refresh()
    assert app.stat_refresh_rate == 7
    menu.teardown()


def test_main_menu_buttons_stack_vertically() -> None:
    app = DummyApp()
    menu = MainMenu(app)
    menu.setup()
    zs = [btn["pos"][2] for btn in menu.buttons]
    assert zs == sorted(zs, reverse=True)
    assert len(set(zs)) == len(zs)
    menu.teardown()

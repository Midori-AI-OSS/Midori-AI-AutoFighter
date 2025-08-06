from __future__ import annotations

import sys
import types

from pathlib import Path

from unittest.mock import Mock
from unittest.mock import patch

import autofighter.save as save
import autofighter.audio as audio

from autofighter.stats import Stats
from autofighter.menu import MainMenu
from autofighter.menu import ISSUE_URL
from autofighter.menu import LoadRunMenu
from autofighter.menu import OptionsMenu
from autofighter.gui import FRAME_COLOR

EXPECTED_URL = (
    "https://github.com/Midori-AI-OSS/Midori-AI-AutoFighter/issues/"
    "new?template=feedback.md&title=Feedback"
)

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


def test_load_run_menu_lists_runs(tmp_path: Path) -> None:
    (tmp_path / "run1.json").write_text('{"stats": {"hp": 1, "max_hp": 2}}')
    (tmp_path / "run2.json").write_text("{}")
    app = DummyApp()
    menu = LoadRunMenu(app)
    LoadRunMenu.RUNS_DIR = tmp_path
    runs = menu.available_runs()
    assert [p.name for p, _ in runs] == ["run1.json"]
    assert "HP" in runs[0][1]


def test_load_run_menu_navigation(tmp_path: Path) -> None:
    for i in range(2):
        (tmp_path / f"run{i}.json").write_text('{"stats": {"hp": 1, "max_hp": 2}}')
    app = DummyApp()
    LoadRunMenu.RUNS_DIR = tmp_path
    menu = LoadRunMenu(app)
    menu.setup()
    highlight = (0.2, 0.2, 0.2, 0.9)
    menu.next()
    assert menu.index == 1
    assert menu.buttons[1]["frameColor"] == highlight
    assert menu.buttons[0]["frameColor"] == FRAME_COLOR
    menu.prev()
    assert menu.buttons[0]["frameColor"] == highlight
    menu.teardown()


def test_load_run_menu_start_run(tmp_path: Path) -> None:
    run_file = tmp_path / "run.json"
    run_file.write_text('{"stats": {"hp": 3, "max_hp": 5}}')

    class SceneManager:
        def __init__(self) -> None:
            self.scene = None

        def switch_to(self, scene) -> None:
            self.scene = scene

    app = DummyApp()
    app.scene_manager = SceneManager()

    class DummyBattle:
        def __init__(self, *_, player, **__):
            self.player = player

    sys.modules['autofighter.battle_room'] = types.SimpleNamespace(BattleRoom=DummyBattle)

    menu = LoadRunMenu(app)
    menu.start_run(run_file)

    assert isinstance(app.scene_manager.scene, DummyBattle)
    assert app.scene_manager.scene.player.hp == 3

    del sys.modules['autofighter.battle_room']


def test_options_menu_volume_arrows_update_audio(tmp_path: Path) -> None:
    save.SETTINGS_PATH = tmp_path / "settings.json"
    class DummyAssets:
        def load(self, *_: object) -> object:
            return object()

    audio._global_audio = audio.AudioManager(DummyAssets())

    app = DummyApp()
    menu = OptionsMenu(app)
    menu.setup()
    menu.increase()
    assert audio.get_audio().sfx_volume == 0.55
    menu.decrease()
    assert audio.get_audio().sfx_volume == 0.5
    menu.next()
    menu.decrease()
    assert audio.get_audio().music_volume == 0.45
    menu.teardown()
    audio._global_audio = None


def test_options_menu_updates_refresh_rate(tmp_path: Path) -> None:
    save.SETTINGS_PATH = tmp_path / "settings.json"
    app = DummyApp()
    menu = OptionsMenu(app)
    menu.setup()
    menu.refresh_slider["value"] = 7
    menu.update_refresh()
    assert app.stat_refresh_rate == 7
    menu.teardown()


def test_main_menu_buttons_form_grid() -> None:
    app = DummyApp()
    menu = MainMenu(app)
    menu.setup()
    positions = [btn["pos"] for btn in menu.buttons]
    xs = sorted({round(p[0], 2) for p in positions})
    zs = sorted({round(p[2], 2) for p in positions}, reverse=True)
    assert len(xs) == 2
    assert len(zs) == 3
    menu.teardown()


def test_main_menu_feedback_opens_issue() -> None:
    assert ISSUE_URL == EXPECTED_URL
    app = DummyApp()
    menu = MainMenu(app)
    with patch("webbrowser.open") as mock_open:
        menu.give_feedback()
    mock_open.assert_called_once_with(ISSUE_URL)


def test_main_menu_feedback_prints_url_when_browser_unavailable(capsys) -> None:
    app = DummyApp()
    menu = MainMenu(app)
    with patch("webbrowser.open", side_effect=Exception):
        menu.give_feedback()
    captured = capsys.readouterr()
    assert ISSUE_URL in captured.out


def test_main_menu_new_run_starts_battle() -> None:
    class SceneManager:
        def __init__(self) -> None:
            self.scene = None

        def switch_to(self, scene) -> None:
            self.scene = scene

    app = DummyApp()
    app.scene_manager = SceneManager()

    dummy_player = ("body", "hair", "color", "acc", Stats(hp=5, max_hp=5), {})

    class DummyBattle:
        def __init__(self, *_: object, player: Stats, **__: object) -> None:
            self.player = player

    sys.modules['autofighter.battle_room'] = types.SimpleNamespace(BattleRoom=DummyBattle)
    with patch("autofighter.menu.load_player", return_value=dummy_player):
        menu = MainMenu(app)
        menu.new_run()

    assert isinstance(app.scene_manager.scene, DummyBattle)
    assert app.scene_manager.scene.player.hp == 5
    del sys.modules['autofighter.battle_room']


def test_main_menu_new_run_without_player_prints_warning(capsys) -> None:
    class SceneManager:
        def __init__(self) -> None:
            self.called = False

        def switch_to(self, *_: object) -> None:
            self.called = True

    app = DummyApp()
    app.scene_manager = SceneManager()

    sys.modules['autofighter.battle_room'] = types.SimpleNamespace(BattleRoom=object)
    with patch("autofighter.menu.load_player", return_value=None):
        menu = MainMenu(app)
        menu.new_run()
    del sys.modules['autofighter.battle_room']

    captured = capsys.readouterr()
    assert "Use Edit Player first" in captured.out
    assert not app.scene_manager.called


def test_main_menu_load_run_switches_scene() -> None:
    class SceneManager:
        def __init__(self) -> None:
            self.scene = None

        def switch_to(self, scene) -> None:
            self.scene = scene

    app = DummyApp()
    app.scene_manager = SceneManager()
    menu = MainMenu(app)
    menu.load_run()
    assert isinstance(app.scene_manager.scene, LoadRunMenu)


def test_main_menu_open_options_switches_scene() -> None:
    class SceneManager:
        def __init__(self) -> None:
            self.scene = None

        def switch_to(self, scene) -> None:
            self.scene = scene

    app = DummyApp()
    app.scene_manager = SceneManager()
    menu = MainMenu(app)
    menu.open_options()
    assert isinstance(app.scene_manager.scene, OptionsMenu)


def test_main_menu_quit_calls_user_exit() -> None:
    called = Mock()

    app = DummyApp()
    app.userExit = called
    menu = MainMenu(app)
    menu.setup()
    menu.index = len(menu.buttons) - 1
    menu.activate()
    called.assert_called_once()
    menu.teardown()

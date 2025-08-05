from __future__ import annotations

from pathlib import Path

try:
    from direct.gui.DirectGui import DirectButton
    from direct.gui.DirectGui import DirectCheckButton
    from direct.gui.DirectGui import DirectSlider
    from direct.showbase.ShowBase import ShowBase
except Exception:  # pragma: no cover - fallback for headless tests
    class _Widget:
        """Minimal widget stand-ins for headless tests."""

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

    class DirectCheckButton(_Widget):  # type: ignore[dead-code]
        def setIndicatorValue(self, value: bool, *_args: object, **_kwargs: object) -> None:
            self.options["indicatorValue"] = value

    class DirectSlider(_Widget):  # type: ignore[dead-code]
        def command(self) -> None:  # pragma: no cover - optional callback
            pass

    class ShowBase:  # type: ignore[dead-code]
        pass

from autofighter.gui import set_widget_pos
from autofighter.save import load_player
from autofighter.save import load_run
from autofighter.scene import Scene


class MainMenu(Scene):
    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.buttons: list[DirectButton] = []
        self.index = 0

    BUTTON_SPACING = 0.25

    def setup(self) -> None:
        labels = [
            ("New Run", self.new_run),
            ("Load Run", self.load_run),
            ("Edit Player", self.edit_player),
            ("Options", self.open_options),
            ("Quit", self.app.userExit),
        ]
        top = self.BUTTON_SPACING * (len(labels) - 1) / 2
        for i, (text, cmd) in enumerate(labels):
            button = DirectButton(
                text=text,
                command=cmd,
                scale=0.1,
                frameColor=(0, 0, 0, 0.5),
                text_fg=(1, 1, 1, 1),
            )
            set_widget_pos(button, (0, 0, top - i * self.BUTTON_SPACING))
            self.buttons.append(button)
        self.highlight()
        self.app.accept("arrow_up", self.prev)
        self.app.accept("arrow_down", self.next)
        self.app.accept("enter", self.activate)

    def teardown(self) -> None:
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        self.app.ignore("arrow_up")
        self.app.ignore("arrow_down")
        self.app.ignore("enter")

    def highlight(self) -> None:
        for i, button in enumerate(self.buttons):
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else (0, 0, 0, 0.5)
            button["frameColor"] = color

    def prev(self) -> None:
        self.index = (self.index - 1) % len(self.buttons)
        self.highlight()

    def next(self) -> None:
        self.index = (self.index + 1) % len(self.buttons)
        self.highlight()

    def activate(self) -> None:
        self.buttons[self.index]["command"]()

    def new_run(self) -> None:
        from autofighter.battle_room import BattleRoom  # local import to defer Panda3D dependency
        loaded = load_player()
        if not loaded:
            print("No saved player. Use Edit Player first.")
            return
        _, _, _, _, stats, _ = loaded
        battle = BattleRoom(self.app, return_scene_factory=lambda: MainMenu(self.app), player=stats)
        self.app.scene_manager.switch_to(battle)

    def load_run(self) -> None:
        self.app.scene_manager.switch_to(LoadRunMenu(self.app))

    def edit_player(self) -> None:
        from autofighter.player_creator import PlayerCreator  # local import to defer Panda3D dependency
        creator = PlayerCreator(
            self.app,
            return_scene_factory=lambda: MainMenu(self.app),
        )
        self.app.scene_manager.switch_to(creator)

    def open_options(self) -> None:
        self.app.scene_manager.switch_to(OptionsMenu(self.app))


class LoadRunMenu(Scene):
    RUNS_DIR = Path("runs")

    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.buttons: list[DirectButton] = []
        self.index = 0

    def available_runs(self) -> list[Path]:
        return sorted(self.RUNS_DIR.glob("*.json"))

    BUTTON_SPACING = 0.25

    def setup(self) -> None:
        runs = self.available_runs()
        labels = [(p.stem, lambda p=p: self.start_run(p)) for p in runs]
        labels.append(("Back", self.back))
        top = self.BUTTON_SPACING * (len(labels) - 1) / 2
        for i, (text, cmd) in enumerate(labels):
            button = DirectButton(
                text=text,
                command=cmd,
                scale=0.1,
                frameColor=(0, 0, 0, 0.5),
                text_fg=(1, 1, 1, 1),
            )
            set_widget_pos(button, (0, 0, top - i * self.BUTTON_SPACING))
            self.buttons.append(button)
        self.highlight()
        self.app.accept("arrow_up", self.prev)
        self.app.accept("arrow_down", self.next)
        self.app.accept("enter", self.activate)
        self.app.accept("escape", self.back)

    def teardown(self) -> None:
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        self.app.ignore("arrow_up")
        self.app.ignore("arrow_down")
        self.app.ignore("enter")
        self.app.ignore("escape")

    def highlight(self) -> None:
        for i, button in enumerate(self.buttons):
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else (0, 0, 0, 0.5)
            button["frameColor"] = color

    def prev(self) -> None:
        self.index = (self.index - 1) % len(self.buttons)
        self.highlight()

    def next(self) -> None:
        self.index = (self.index + 1) % len(self.buttons)
        self.highlight()

    def activate(self) -> None:
        self.buttons[self.index]["command"]()

    def start_run(self, path: Path) -> None:
        from autofighter.battle_room import BattleRoom  # local import to defer Panda3D dependency

        stats = load_run(path)
        if not stats:
            print(f"Run file {path} missing or invalid")
            return
        battle = BattleRoom(self.app, return_scene_factory=lambda: MainMenu(self.app), player=stats)
        self.app.scene_manager.switch_to(battle)

    def back(self) -> None:
        self.app.scene_manager.switch_to(MainMenu(self.app))

class OptionsMenu(Scene):
    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.widgets: list[DirectButton | DirectCheckButton | DirectSlider] = []
        self.index = 0
        self.sfx_volume = 0.5
        self.music_volume = 0.5
        self.stat_refresh_rate = getattr(self.app, "stat_refresh_rate", 5)
        self.pause_on_stats = getattr(self.app, "pause_on_stats", True)

    BUTTON_SPACING = 0.3

    def setup(self) -> None:
        self.sfx_slider = DirectSlider(
            range=(0, 1),
            value=self.sfx_volume,
            scale=0.5,
            frameColor=(0, 0, 0, 0.5),
            command=self.update_sfx,
        )
        self.music_slider = DirectSlider(
            range=(0, 1),
            value=self.music_volume,
            scale=0.5,
            frameColor=(0, 0, 0, 0.5),
            command=self.update_music,
        )
        self.refresh_slider = DirectSlider(
            range=(1, 10),
            value=self.stat_refresh_rate,
            scale=0.5,
            frameColor=(0, 0, 0, 0.5),
            command=self.update_refresh,
        )
        self._pause_button = DirectCheckButton(
            text="Pause on Stat Screen",
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
            indicatorValue=self.pause_on_stats,
            command=self.toggle_pause,
        )
        self._back_button = DirectButton(
            text="Back",
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
            command=self.back,
        )
        self.widgets = [
            self.sfx_slider,
            self.music_slider,
            self.refresh_slider,
            self._pause_button,
            self._back_button,
        ]
        top = self.BUTTON_SPACING * (len(self.widgets) - 1) / 2
        for i, widget in enumerate(self.widgets):
            set_widget_pos(widget, (0, 0, top - i * self.BUTTON_SPACING))
        self.highlight()
        self.app.accept("arrow_up", self.prev)
        self.app.accept("arrow_down", self.next)
        self.app.accept("arrow_left", self.decrease)
        self.app.accept("arrow_right", self.increase)
        self.app.accept("enter", self.activate)
        self.app.accept("escape", self.back)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.app.ignore("arrow_up")
        self.app.ignore("arrow_down")
        self.app.ignore("arrow_left")
        self.app.ignore("arrow_right")
        self.app.ignore("enter")
        self.app.ignore("escape")

    def highlight(self) -> None:
        for i, widget in enumerate(self.widgets):
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else (0, 0, 0, 0.5)
            widget["frameColor"] = color

    def prev(self) -> None:
        self.index = (self.index - 1) % len(self.widgets)
        self.highlight()

    def next(self) -> None:
        self.index = (self.index + 1) % len(self.widgets)
        self.highlight()

    def activate(self) -> None:
        widget = self.widgets[self.index]
        if widget == self.back_button:
            self.back()
        elif widget == self.pause_button:
            self.pause_button.setIndicatorValue(not self.pause_button["indicatorValue"])
            self.toggle_pause()

    def decrease(self) -> None:
        widget = self.widgets[self.index]
        if isinstance(widget, DirectSlider):
            min_val, max_val = widget["range"]
            step = 0.05 if max_val <= 1 else 1
            widget["value"] = max(min_val, widget["value"] - step)
            widget.command()

    def increase(self) -> None:
        widget = self.widgets[self.index]
        if isinstance(widget, DirectSlider):
            min_val, max_val = widget["range"]
            step = 0.05 if max_val <= 1 else 1
            widget["value"] = min(max_val, widget["value"] + step)
            widget.command()

    def update_sfx(self) -> None:
        self.sfx_volume = float(self.sfx_slider["value"])
        for mgr in getattr(self.app, "sfxManagerList", []):
            mgr.setVolume(self.sfx_volume)

    def update_music(self) -> None:
        self.music_volume = float(self.music_slider["value"])
        mgr = getattr(self.app, "musicManager", None)
        if mgr is not None:
            mgr.setVolume(self.music_volume)

    def update_refresh(self) -> None:
        self.stat_refresh_rate = int(self.refresh_slider["value"])
        self.app.stat_refresh_rate = self.stat_refresh_rate

    def toggle_pause(self, _=None) -> None:
        self.pause_on_stats = bool(self.pause_button["indicatorValue"])
        self.app.pause_on_stats = self.pause_on_stats

    def back(self) -> None:
        self.app.scene_manager.switch_to(MainMenu(self.app))

    @property
    def pause_button(self) -> DirectCheckButton:
        return self._pause_button

    @property
    def back_button(self) -> DirectButton:
        return self._back_button

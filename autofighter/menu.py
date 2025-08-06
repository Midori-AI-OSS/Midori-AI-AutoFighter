from __future__ import annotations

import math
import webbrowser

from pathlib import Path

try:
    from direct.gui.DirectGui import DirectButton
    from direct.gui.DirectGui import DirectCheckButton
    from direct.gui.DirectGui import DirectFrame
    from direct.gui.DirectGui import DirectLabel
    from direct.gui.DirectGui import DirectSlider
    from direct.gui import DirectGuiGlobals as DGG
    from direct.showbase.ShowBase import ShowBase
    from panda3d.core import CardMaker
    from panda3d.core import TextureStage
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

        def bind(self, *_args: object, **_kwargs: object) -> None:
            pass

        def unbind(self, *_args: object, **_kwargs: object) -> None:
            pass

    class DirectButton(_Widget):  # type: ignore[dead-code]
        pass

    class DirectCheckButton(_Widget):  # type: ignore[dead-code]
        def setIndicatorValue(self, value: bool, *_args: object, **_kwargs: object) -> None:
            self.options["indicatorValue"] = value

    class DirectFrame(_Widget):  # type: ignore[dead-code]
        pass

    class DirectLabel(_Widget):  # type: ignore[dead-code]
        pass

    class DirectSlider(_Widget):  # type: ignore[dead-code]
        def command(self) -> None:  # pragma: no cover - optional callback
            func = self.options.get("command")
            if callable(func):
                func()

    class ShowBase:  # type: ignore[dead-code]
        pass

    class CardMaker:  # type: ignore[dead-code]
        def setFrame(self, *_args: object) -> None:
            pass

        def generate(self) -> object:
            return object()

    class TextureStage:  # type: ignore[dead-code]
        @staticmethod
        def getDefault() -> object:
            return object()

from autofighter.gui import FRAME_COLOR
from autofighter.gui import SLIDER_SCALE
from autofighter.gui import TEXT_COLOR
from autofighter.gui import WIDGET_SCALE
from autofighter.gui import set_widget_pos
from autofighter.save import load_run
from autofighter.save import load_player
from autofighter.save import save_settings
from autofighter.audio import get_audio
from autofighter.scene import Scene
from autofighter.assets import AssetManager


ISSUE_URL = (
    "https://github.com/Midori-AI-OSS/Midori-AI-AutoFighter/issues/"
    "new?template=feedback.md&title=Feedback"
)


ASSETS = AssetManager()


def add_tooltip(widget: DirectFrame | DirectButton | DirectSlider | DirectCheckButton, text: str) -> None:
    try:
        tooltip = DirectLabel(
            text=text,
            text_fg=TEXT_COLOR,
            frameColor=FRAME_COLOR,
            scale=WIDGET_SCALE,
            parent=widget,
            pos=(0, 0, -0.2),
        )
        tooltip.hide()
        widget.bind(DGG.ENTER, lambda *_: tooltip.show())
        widget.bind(DGG.EXIT, lambda *_: tooltip.hide())
    except Exception:  # pragma: no cover - headless tests
        pass


class MainMenu(Scene):
    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.buttons: list[DirectButton] = []
        self.index = 0
        self.bg = None

    BUTTON_SPACING_X = 0.6
    BUTTON_SPACING_Y = 0.4

    def setup(self) -> None:
        if hasattr(self.app, "disableMouse"):
            try:
                self.app.disableMouse()
            except Exception:  # pragma: no cover
                pass
        if hasattr(self.app, "render2d") and hasattr(self.app, "taskMgr"):
            try:
                tex = ASSETS.load("textures", "icon_refresh_cw")  # dummy texture for bg
                cm = CardMaker("bg")
                cm.setFrame(-1, 1, -1, 1)
                self.bg = self.app.render2d.attachNewNode(cm.generate())
                self.bg.setTexture(tex)
                self.bg.setBin("background", 0)
                self.bg.setDepthWrite(False)
                self.bg.setDepthTest(False)
                self.bg_offset = 0.0

                def _animate_bg(task):
                    self.bg_offset += 0.0005
                    ts = TextureStage.getDefault()
                    self.bg.setTexOffset(ts, self.bg_offset, self.bg_offset)
                    r = 0.5 + 0.5 * math.sin(self.bg_offset)
                    g = 0.5 + 0.5 * math.sin(self.bg_offset + 2)
                    b = 0.5 + 0.5 * math.sin(self.bg_offset + 4)
                    self.bg.setColorScale(r, g, b, 1)
                    return task.cont

                self.app.taskMgr.add(_animate_bg, "main-menu-bg")
            except Exception:  # pragma: no cover - skip if Panda3D missing
                self.bg = None
        buttons = [
            ("New Run", "icon_play", self.new_run),
            ("Load Run", "icon_folder_open", self.load_run),
            ("Edit Player", "icon_user", self.edit_player),
            ("Options", "icon_settings", self.open_options),
            ("Give Feedback", "icon_message_square", self.give_feedback),
            ("Quit", "icon_power", self.app.userExit),
        ]
        cols = 2
        for i, (label, icon_name, cmd) in enumerate(buttons):
            img = ASSETS.load("textures", icon_name)
            button = DirectButton(
                text=label,
                command=cmd,
                scale=WIDGET_SCALE * 1.5,
                frameColor=FRAME_COLOR,
                text_fg=TEXT_COLOR,
                image=img,
                image_scale=WIDGET_SCALE,
                text_pos=(0, -0.12),
            )
            col = i % cols
            row = i // cols
            x = (col - (cols - 1) / 2) * self.BUTTON_SPACING_X
            y = ((len(buttons) // cols - 1) / 2 - row) * self.BUTTON_SPACING_Y
            set_widget_pos(button, (x, 0, y))
            add_tooltip(button, label)
            self.buttons.append(button)
        self.highlight()
        self.app.accept("arrow_up", self.prev)
        self.app.accept("arrow_down", self.next)
        self.app.accept("arrow_left", self.left)
        self.app.accept("arrow_right", self.right)
        self.app.accept("enter", self.activate)

    def teardown(self) -> None:
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        self.app.ignore("arrow_up")
        self.app.ignore("arrow_down")
        self.app.ignore("arrow_left")
        self.app.ignore("arrow_right")
        self.app.ignore("enter")
        if self.bg is not None and hasattr(self.bg, "removeNode"):
            self.bg.removeNode()
        if hasattr(self.app, "taskMgr"):
            try:
                self.app.taskMgr.remove("main-menu-bg")
            except Exception:  # pragma: no cover
                pass

    def highlight(self) -> None:
        for i, button in enumerate(self.buttons):
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else FRAME_COLOR
            button["frameColor"] = color

    def move(self, dx: int, dy: int) -> None:
        cols = 2
        rows = 3
        row = self.index // cols
        col = self.index % cols
        row = (row + dy) % rows
        col = (col + dx) % cols
        self.index = row * cols + col
        self.highlight()

    def prev(self) -> None:
        self.move(0, -1)

    def next(self) -> None:
        self.move(0, 1)

    def left(self) -> None:
        self.move(-1, 0)

    def right(self) -> None:
        self.move(1, 0)

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

    def give_feedback(self) -> None:
        try:
            webbrowser.open(ISSUE_URL)
        except Exception:
            print(f"Open this page to give feedback: {ISSUE_URL}")

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

    def available_runs(self) -> list[tuple[Path, str]]:
        runs: list[tuple[Path, str]] = []
        for path in sorted(self.RUNS_DIR.glob("*.json")):
            stats = load_run(path)
            if stats:
                label = f"{path.stem}: HP {stats.hp}/{stats.max_hp}"
                runs.append((path, label))
        return runs

    BUTTON_SPACING = 0.25

    def setup(self) -> None:
        runs = self.available_runs()
        labels = [(label, lambda p=p: self.start_run(p)) for p, label in runs]
        labels.append(("Back", self.back))
        top = self.BUTTON_SPACING * (len(labels) - 1) / 2
        for i, (text, cmd) in enumerate(labels):
            button = DirectButton(
                text=text,
                command=cmd,
                scale=WIDGET_SCALE,
                frameColor=FRAME_COLOR,
                text_fg=TEXT_COLOR,
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
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else FRAME_COLOR
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
        audio_mgr = get_audio()
        self.sfx_volume = audio_mgr.sfx_volume
        self.music_volume = audio_mgr.music_volume
        self.stat_refresh_rate = getattr(self.app, "stat_refresh_rate", 5)
        self.pause_on_stats = getattr(self.app, "pause_on_stats", True)

    BUTTON_SPACING = 0.3

    def setup(self) -> None:
        self.sfx_slider = DirectSlider(
            range=(0, 1),
            value=self.sfx_volume,
            scale=SLIDER_SCALE,
            frameColor=FRAME_COLOR,
            command=self.update_sfx,
        )
        DirectFrame(
            parent=self.sfx_slider,
            image=ASSETS.load("textures", "icon_volume_2"),
            frameColor=(0, 0, 0, 0),
            scale=WIDGET_SCALE,
            pos=(-0.7, 0, 0),
        )
        DirectLabel(
            parent=self.sfx_slider,
            text="SFX Volume",
            text_fg=TEXT_COLOR,
            frameColor=(0, 0, 0, 0),
            scale=WIDGET_SCALE,
            pos=(-0.3, 0, 0),
        )
        add_tooltip(self.sfx_slider, "Adjust sound effect volume.")

        self.music_slider = DirectSlider(
            range=(0, 1),
            value=self.music_volume,
            scale=SLIDER_SCALE,
            frameColor=FRAME_COLOR,
            command=self.update_music,
        )
        DirectFrame(
            parent=self.music_slider,
            image=ASSETS.load("textures", "icon_music"),
            frameColor=(0, 0, 0, 0),
            scale=WIDGET_SCALE,
            pos=(-0.7, 0, 0),
        )
        DirectLabel(
            parent=self.music_slider,
            text="Music Volume",
            text_fg=TEXT_COLOR,
            frameColor=(0, 0, 0, 0),
            scale=WIDGET_SCALE,
            pos=(-0.3, 0, 0),
        )
        add_tooltip(self.music_slider, "Adjust background music volume.")

        self.refresh_slider = DirectSlider(
            range=(1, 10),
            value=self.stat_refresh_rate,
            scale=SLIDER_SCALE,
            frameColor=FRAME_COLOR,
            command=self.update_refresh,
        )
        DirectFrame(
            parent=self.refresh_slider,
            image=ASSETS.load("textures", "icon_refresh_cw"),
            frameColor=(0, 0, 0, 0),
            scale=WIDGET_SCALE,
            pos=(-0.7, 0, 0),
        )
        DirectLabel(
            parent=self.refresh_slider,
            text="Refresh Rate",
            text_fg=TEXT_COLOR,
            frameColor=(0, 0, 0, 0),
            scale=WIDGET_SCALE,
            pos=(-0.3, 0, 0),
        )
        add_tooltip(self.refresh_slider, "Update stats every N frames.")

        self._pause_button = DirectCheckButton(
            text="Pause on Stat Screen",
            frameColor=FRAME_COLOR,
            text_fg=TEXT_COLOR,
            indicatorValue=self.pause_on_stats,
            command=self.toggle_pause,
            scale=WIDGET_SCALE,
        )
        DirectFrame(
            parent=self._pause_button,
            image=ASSETS.load("textures", "icon_pause"),
            frameColor=(0, 0, 0, 0),
            scale=WIDGET_SCALE,
            pos=(-1.2, 0, 0),
        )
        add_tooltip(self._pause_button, "Stop gameplay while viewing stats.")

        self._back_button = DirectButton(
            text="Back",
            frameColor=FRAME_COLOR,
            text_fg=TEXT_COLOR,
            command=self.back,
            scale=WIDGET_SCALE,
        )
        add_tooltip(self._back_button, "Return to main menu.")
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
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else FRAME_COLOR
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
        get_audio().set_sfx_volume(self.sfx_volume)
        save_settings(self._settings_payload())

    def update_music(self) -> None:
        self.music_volume = float(self.music_slider["value"])
        get_audio().set_music_volume(self.music_volume)
        save_settings(self._settings_payload())

    def update_refresh(self) -> None:
        self.stat_refresh_rate = int(self.refresh_slider["value"])
        self.app.stat_refresh_rate = self.stat_refresh_rate
        save_settings(self._settings_payload())

    def toggle_pause(self, _=None) -> None:
        self.pause_on_stats = bool(self.pause_button["indicatorValue"])
        self.app.pause_on_stats = self.pause_on_stats
        save_settings(self._settings_payload())

    def back(self) -> None:
        self.app.scene_manager.switch_to(MainMenu(self.app))

    @property
    def pause_button(self) -> DirectCheckButton:
        return self._pause_button

    @property
    def back_button(self) -> DirectButton:
        return self._back_button

    def _settings_payload(self) -> dict[str, object]:
        return {
            "sfx_volume": self.sfx_volume,
            "music_volume": self.music_volume,
            "stat_refresh_rate": self.stat_refresh_rate,
            "pause_on_stats": self.pause_on_stats,
        }

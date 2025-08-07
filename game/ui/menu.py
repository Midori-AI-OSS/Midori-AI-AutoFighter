from __future__ import annotations

import math
import webbrowser

from pathlib import Path

try:
    from direct.gui import DirectGuiGlobals as DGG
    from direct.gui.DirectGui import DirectButton
    from direct.gui.DirectGui import DirectCheckButton
    from direct.gui.DirectGui import DirectFrame
    from direct.gui.DirectGui import DirectLabel
    from direct.gui.DirectGui import DirectSlider
    from direct.showbase.ShowBase import ShowBase
    from panda3d.core import CardMaker
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

from .options import OptionsMenu
from .party_picker import PartyPicker
from autofighter.gui import FRAME_COLOR
from autofighter.gui import TEXT_COLOR
from autofighter.gui import get_widget_scale
from autofighter.gui import set_widget_pos
from autofighter.scene import Scene
from autofighter.save import load_player
from autofighter.save import load_run
from autofighter.assets import get_texture
from autofighter.assets import get_player_photo


ISSUE_URL = (
    "https://github.com/Midori-AI-OSS/Midori-AI-AutoFighter/issues/"
    "new?template=feedback.md&title=Feedback"
)


def add_tooltip(widget: DirectFrame | DirectButton | DirectSlider | DirectCheckButton, text: str) -> None:
    try:
        tooltip = DirectLabel(
            text=text,
            text_fg=TEXT_COLOR,
            frameColor=FRAME_COLOR,
            scale=get_widget_scale(),
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
        self.top_bar = None
        self.banner = None
        self.avatar = None
        self.corner_buttons: list[DirectButton] = []
        self._feedback_label = None

    def setup(self) -> None:
        if hasattr(self.app, "disableMouse"):
            try:
                self.app.disableMouse()
            except Exception:  # pragma: no cover
                pass
        if hasattr(self.app, "render2d") and hasattr(self.app, "taskMgr"):
            try:
                try:
                    tex = get_texture("menu_bg")
                except Exception:
                    tex = get_texture("white")
                cm = CardMaker("bg")
                cm.setFrame(-1, 1, -1, 1)
                self.bg = self.app.render2d.attachNewNode(cm.generate())
                self.bg.setTexture(tex)
                self.bg.setBin("background", 0)
                self.bg.setDepthWrite(False)
                self.bg.setDepthTest(False)
                self.bg.setColorScale(0.2, 0.2, 0.2, 1)
            except Exception:  # pragma: no cover - skip if Panda3D missing
                self.bg = None
        try:
            self.top_bar = DirectFrame(frameColor=FRAME_COLOR, scale=get_widget_scale())
            set_widget_pos(self.top_bar, (0, 0, 0.9))
            try:
                photo = get_player_photo("becca")
            except Exception:
                photo = get_texture("white")
            self.avatar = DirectButton(
                image=photo,
                frameColor=(0, 0, 0, 0),
                scale=get_widget_scale(),
                parent=self.top_bar,
            )
            set_widget_pos(self.avatar, (-0.95, 0, 0))
            DirectLabel(
                text="Player",
                text_fg=TEXT_COLOR,
                frameColor=(0, 0, 0, 0),
                parent=self.top_bar,
                pos=(-0.85, 0, 0),
            )
            DirectLabel(
                text="Gold: 0 | Tickets: 0",
                text_fg=TEXT_COLOR,
                frameColor=(0, 0, 0, 0),
                parent=self.top_bar,
                pos=(0.2, 0, 0),
            )
            try:
                banner_tex = get_texture("menu_bg")
            except Exception:
                banner_tex = get_texture("white")
            self.banner = DirectButton(
                image=banner_tex,
                frameColor=(0, 0, 0, 0),
                scale=get_widget_scale() * 2,
            )
            set_widget_pos(self.banner, (0, 0, 0.3))
            for icon, pos in [
                ("icon_message_square", (-0.9, 0, 0.9)),
                ("icon_folder_open", (0.9, 0, 0.9)),
            ]:
                img = get_texture(icon)
                btn = DirectButton(image=img, scale=get_widget_scale())
                set_widget_pos(btn, pos)
                self.corner_buttons.append(btn)
        except Exception:  # pragma: no cover - headless tests
            self.top_bar = None
            self.banner = None
            self.avatar = None
            self.corner_buttons = []
        buttons = [
            ("New Run", "icon_play", self.new_run),
            ("Load Run", "icon_folder_open", self.load_run),
            ("Edit Player", "icon_user", self.edit_player),
            ("Options", "icon_settings", self.open_options),
            ("Give Feedback", "icon_message_square", self.give_feedback),
            ("Quit", "icon_power", self.app.userExit),
        ]
        cols = 2
        rows = math.ceil(len(buttons) / cols)
        button_scale = get_widget_scale() * 1.5
        image_scale = get_widget_scale()
        x_positions = [-0.4, 0.4]
        y_base = -0.8
        y_spacing = 0.25
        for i, (label, icon_name, cmd) in enumerate(buttons):
            img = get_texture(icon_name)
            button = DirectButton(
                text=label,
                command=cmd,
                scale=button_scale,
                frameColor=FRAME_COLOR,
                text_fg=TEXT_COLOR,
                image=img,
                image_scale=image_scale,
                text_pos=(0, -0.12),
            )
            col = i % cols
            row = i // cols
            x = x_positions[col]
            y = y_base + row * y_spacing
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
        for button in self.corner_buttons:
            button.destroy()
        self.corner_buttons.clear()
        if self.top_bar is not None:
            self.top_bar.destroy()
            self.top_bar = None
            self.avatar = None
        if self.banner is not None:
            self.banner.destroy()
            self.banner = None
        self.app.ignore("arrow_up")
        self.app.ignore("arrow_down")
        self.app.ignore("arrow_left")
        self.app.ignore("arrow_right")
        self.app.ignore("enter")
        if self.bg is not None and hasattr(self.bg, "removeNode"):
            self.bg.removeNode()
        if self._feedback_label is not None:
            self._feedback_label.destroy()
            self._feedback_label = None

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
        loaded = load_player()
        if not loaded:
            print("No saved player. Use Edit Player first.")
            return
        _, _, _, _, stats, _ = loaded
        picker = PartyPicker(self.app, stats)
        self.app.scene_manager.switch_to(picker)

    def load_run(self) -> None:
        self.app.scene_manager.switch_to(LoadRunMenu(self.app))

    def give_feedback(self) -> None:
        try:
            webbrowser.open(ISSUE_URL)
        except Exception:
            self._feedback_label = DirectLabel(
                text=f"Open this page to give feedback:\n{ISSUE_URL}",
                text_fg=TEXT_COLOR,
                frameColor=FRAME_COLOR,
                scale=get_widget_scale(),
            )

    def edit_player(self) -> None:
        from autofighter.player_creator import PlayerCreator  # local import to defer Panda3D dependency
        creator = PlayerCreator(
            self.app,
            return_scene_factory=lambda: MainMenu(self.app),
        )
        self.app.scene_manager.switch_to(creator)

    def open_options(self) -> None:
        self.app.scene_manager.switch_to(OptionsMenu(self.app))

    @property
    def feedback_label(self) -> DirectLabel | None:
        return self._feedback_label


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
                scale=get_widget_scale(),
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


from __future__ import annotations

import json
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
            scale=1.0,
            text_scale=0.04,
            parent=widget,
            pos=(0, 0, -0.2),
        )
        tooltip.hide()
        widget.bind(DGG.ENTER, lambda *_: tooltip.show())
        widget.bind(DGG.EXIT, lambda *_: tooltip.hide())
    except Exception:  # pragma: no cover - headless tests
        pass


class MainMenu(Scene):
    # Placeholder: In the future, set banner text to 'Load Run' if the player has a run in progress, otherwise 'New Run'.
    # Example:
    # if self.player_has_run():
    #     self.banner_label['text'] = 'Load Run'
    # else:
    #     self.banner_label['text'] = 'New Run'
    # --- Button callback placeholders ---
    def home_button(self):
        print("Home button pressed")

    def pulls_button(self):
        print("Pulls button pressed")

    def crafting_button(self):
        print("Crafting button pressed")

    def edit_player(self):
        print("Edit Player button pressed")

    def edit_team(self):
        print("Edit Team button pressed")

    def open_options(self):
        print("Settings button pressed")

    def exit_game(self):
        if hasattr(self.app, 'userExit'):
            self.app.userExit()
        else:
            print("Exit called, but no userExit method on app.")
    def __init__(self, app: ShowBase) -> None:
        print("MainMenu.__init__ called")
        self.app = app
        self.buttons: list[DirectButton] = []
        self.index = 0
        self.bg = None
        self.top_bar = None
        self.banner = None
        self.avatar = None
        self.corner_buttons: list[DirectButton] = []
        self.top_left_buttons: list[DirectButton] = []
        self._feedback_label = None

    def setup(self) -> None:
        print("MainMenu.setup called")
        """Set up the main menu UI in a single, robust method."""
        if hasattr(self.app, "disableMouse"):
            try:
                self.app.disableMouse()
            except Exception:
                pass
        self.setup_ui()

    def setup_ui(self) -> None:
        print("MainMenu.setup_ui called")
        """Unified UI setup: background, top bar, banner, button grid, navigation, etc."""
        # --- Parent node setup (always define) ---
        parent_node = getattr(self.app, 'aspect2d', None)
        if parent_node is None:
            try:
                from direct.showbase import ShowBaseGlobal
                base = getattr(ShowBaseGlobal, 'base', None)
                parent_node = getattr(base, 'aspect2d', None)
            except Exception:
                parent_node = None
        # --- Background setup (migrated from setup_background) ---
        try:
            from direct.showbase import ShowBaseGlobal
            base = ShowBaseGlobal.base
            tex = get_texture("menu_bg")
        except Exception:
            tex = get_texture("white")
            base = None
        try:
            from panda3d.core import CardMaker
            cm = CardMaker("bg")
            cm.setFrame(-1, 1, -1, 1)
            if parent_node is not None:
                self.bg = parent_node.attachNewNode(cm.generate())
                self.bg.setTexture(tex)
                self.bg.setBin("background", 0)
                self.bg.setDepthWrite(False)
                self.bg.setDepthTest(False)
                self.bg.setColorScale(0.15, 0.15, 0.2, 1)
            else:
                self.bg = None
        except Exception:
            self.bg = None
        # --- End background setup ---

        # --- Top-left buttons ---
        try:
            button_radius = 0.09
            start_x = -0.9
            start_z = 0.85
            button_spacing = 0.25
            top_buttons = [
                ("Home", self.home_button),
                ("Pulls", self.pulls_button),
                ("Crafting", self.crafting_button),
            ]
            for i, (label, cmd) in enumerate(top_buttons):
                x = start_x + i * button_spacing
                circle = DirectFrame(
                    frameColor=(1, 0, 0, 1),
                    frameSize=(-button_radius, button_radius, -button_radius, button_radius),
                    pos=(x, 0, start_z),
                    relief=None,
                    parent=parent_node,
                )
                btn = DirectButton(
                    frameColor=(1, 1, 1, 0),
                    frameSize=(-button_radius, button_radius, -button_radius, button_radius),
                    relief=None,
                    pos=(x, 0, start_z),
                    scale=1.0,
                    parent=parent_node,
                    command=cmd,
                    text="",
                    rolloverSound=None,
                    clickSound=None,
                )
                self.top_left_buttons.append(btn)
                DirectLabel(
                    text=f"{label} Button",
                    text_fg=(1, 1, 1, 1),
                    frameColor=(0, 0, 0, 0),
                    pos=(x, 0, start_z - button_radius - 0.08),
                    scale=0.06,
                    text_scale=1.0,
                    parent=parent_node,
                )
                add_tooltip(btn, f"{label} Button")
        except Exception:
            pass
        # --- End top-left buttons ---

        # --- Right side: banner and vertical buttons ---
        try:
            # Large banner
            banner = DirectFrame(
                frameColor=(0.8, 0.8, 0.8, 0.4),
                frameSize=(-0.2, 0.2, 0.02, 0.1),
                pos=(0.45, 0, 0.7),
                parent=parent_node,
                scale=1.0,
            )
            # Placeholder: Set text to 'Load Run' if player has a run, else 'New Run'
            self.banner_label = DirectLabel(
                text="New Game / Load Game",
                text_fg=(1, 1, 1, 1),
                frameColor=(0, 0, 0, 0.3),
                parent=banner,
                pos=(0, 0, 0.07),
                scale=0.07,
                text_scale=0.07,
            )
            # Vertical stack of buttons
            right_buttons = [
                ("Edit Player", self.edit_player),
                ("Edit Team", self.edit_team),
                ("Settings", self.open_options),
                ("Exit", self.exit_game),
            ]
            for i, (label, cmd) in enumerate(right_buttons):
                btn = DirectButton(
                    text=label,
                    command=cmd,
                    scale=0.07,
                    text_scale=0.07,
                    frameColor=(0.7, 0.7, 0.7, 0.8),
                    text_fg=(1, 1, 1, 1),
                    frameSize=(-0.18, 0.18, -0.05, 0.05),
                    pos=(0.95, 0, 0.45 - i * 0.12),
                    parent=parent_node,
                )
        except Exception:
            pass
        # --- End right side ---


    def setup_top_bar(self) -> None:
        """Create a frosted-glass top bar with player avatar, name, and currencies, parented to aspect2d."""
        try:
            base = globals().get("base", None)
            parent_node = getattr(base, "aspect2d", None) if base is not None else None
            if parent_node is None:
                parent_node = getattr(self.app, "aspect2d", None)
            if parent_node is None:
                parent_node = getattr(self.app, "render2d", None)
            # Frosted-glass effect with higher alpha and subtle tint
            frosted_color = (0.1, 0.1, 0.15, 0.8)
            self.top_bar = DirectFrame(
                frameColor=frosted_color,
                frameSize=(-1.0, 1.0, -0.08, 0.08),
                scale=get_widget_scale(),
                parent=parent_node,
            )
            set_widget_pos(self.top_bar, (0, 0, 0.92))
            # Player avatar with rounded frame effect - fixed positioning
            try:
                photo = get_player_photo("becca")
            except Exception:
                photo = get_texture("white")
            set_widget_pos(self.banner, (0, 0, 0.3))
        except Exception:
            pass
    def setup_button_grid(self) -> None:
        """Create a 2x3 high-contrast grid of large Lucide icons anchored near the bottom, parented to aspect2d."""
        try:
            from direct.showbase.ShowBase import base
            parent_node = getattr(base, "aspect2d", None)
            if parent_node is None:
                parent_node = getattr(self.app, "aspect2d", None)
            if parent_node is None:
                parent_node = getattr(self.app, "render2d", None)
        except Exception:
            parent_node = None
        buttons = [
            ("New Run", "icon_play", self.new_run),
            ("Load Run", "icon_folder_open", self.load_run),
            ("Edit Player", "icon_user", self.edit_player),
            ("Options", "icon_settings", self.open_options),
            ("Give Feedback", "icon_message_square", self.give_feedback),
            ("Quit", "icon_power", self.app.userExit),
        ]
        cols = 2
        rows = 3
        button_scale = 1.0
        icon_scale = 1.0
        x_positions = [-0.3, 0.3]
        y_base = -0.6
        y_spacing = 0.2
        for i, (label, icon_name, cmd) in enumerate(buttons):
            img = get_texture(icon_name)
            button = DirectButton(
                text=label,
                command=cmd,
                scale=1.0,
                text_scale=0.04,
                parent=parent_node,
            )
            col = i % cols
            row = i // cols
            x = x_positions[col]
            y = y_base + row * y_spacing
            set_widget_pos(button, (x, 0, y))
            add_tooltip(button, label)
            self.buttons.append(button)

    def setup_navigation(self) -> None:
        """Set up keyboard and controller navigation."""
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
        """Highlight the currently selected button with enhanced visual feedback."""
        for i, button in enumerate(self.buttons):
            if i == self.index:
                # Selected button: brighter with accent highlight
                color = (0.25, 0.25, 0.35, 1.0)  # Highlighted state
                button["frameColor"] = color
                # Slightly scale up for visual feedback - using corrected scale
                if hasattr(button, "setScale"):
                    button.setScale(get_widget_scale() * 1.3)  # Reduced from 2.1
            else:
                # Unselected buttons: standard dark frosted-glass
                color = (0.15, 0.15, 0.2, 0.9)
                button["frameColor"] = color
                if hasattr(button, "setScale"):
                    button.setScale(get_widget_scale() * 1.2)  # Reduced from 2.0

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

        # The following lines were incorrectly indented and caused an IndentationError.
        # They should be part of a function, likely available_runs or similar.
        # If this is not the correct function, please move them as needed.

    # Placeholder for available_runs method (fix indentation)
    def available_runs(self):
        runs = []
        # ...existing code to populate runs...
        # Example placeholder:
        # for path, stats in some_source:
        #     label = f"{path.stem}: HP {stats.hp}/{stats.max_hp}"
        #     runs.append((path, label))
        return runs

    BUTTON_SPACING = 0.25

    def teardown(self) -> None:
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        for button in self.top_left_buttons:
            button.destroy()
        self.top_left_buttons.clear()
        for button in self.corner_buttons:
            button.destroy()
        self.corner_buttons.clear()
        self.app.ignore("arrow_up")
        self.app.ignore("arrow_down")
        self.app.ignore("enter")
        self.app.ignore("escape")

    def highlight(self) -> None:
        """Highlight the currently selected button with enhanced visual feedback."""
        for i, button in enumerate(self.buttons):
            if i == self.index:
                # Selected button: brighter with accent highlight
                color = (0.25, 0.25, 0.35, 1.0)  # Highlighted state
                button["frameColor"] = color
            else:
                # Unselected buttons: standard dark frosted-glass
                color = (0.15, 0.15, 0.2, 0.9)
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


class LoadRunMenu(Scene):
    RUNS_DIR = Path("runs")

    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.buttons: list[DirectButton] = []
        self.index = 0

    def available_runs(self) -> list[tuple[Path, str]]:
        runs: list[tuple[Path, str]] = []
        for path in sorted(self.RUNS_DIR.glob("*.json")):
            try:
                data = json.loads(path.read_text())
                stats = data.get("stats") or {}
                hp = stats.get("hp")
                max_hp = stats.get("max_hp")
                if hp is None or max_hp is None:
                    continue
                label = f"{path.name}: HP {hp}/{max_hp}"
                runs.append((path, label))
            except Exception:
                continue
        return runs

    def setup(self) -> None:
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()
        for path, label in self.available_runs():
            btn = DirectButton(text=label, command=lambda p=path: self.start_run(p))
            btn["frameColor"] = FRAME_COLOR
            self.buttons.append(btn)
        self.highlight()

    def highlight(self) -> None:
        highlight = (0.2, 0.2, 0.2, 0.9)
        for i, btn in enumerate(self.buttons):
            btn["frameColor"] = highlight if i == self.index else FRAME_COLOR

    def next(self) -> None:
        if self.buttons:
            self.index = (self.index + 1) % len(self.buttons)
            self.highlight()

    def prev(self) -> None:
        if self.buttons:
            self.index = (self.index - 1) % len(self.buttons)
            self.highlight()

    def start_run(self, path: Path) -> None:
        from autofighter.battle_room import BattleRoom

        stats = load_run(path)
        if not stats:
            return
        battle = BattleRoom(
            self.app,
            return_scene_factory=lambda: MainMenu(self.app),
            player=stats,
        )
        self.app.scene_manager.switch_to(battle)

    def teardown(self) -> None:
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()


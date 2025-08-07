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
        """Set up the Arknights-inspired main menu with frosted-glass panels and high-contrast grid layout."""
        if hasattr(self.app, "disableMouse"):
            try:
                self.app.disableMouse()
            except Exception:  # pragma: no cover
                pass
        
        self.setup_background()
        self.setup_top_bar()
        self.setup_banner()
        self.setup_button_grid()
        self.setup_navigation()

    def setup_background(self) -> None:
        """Create a dark, cloud-like background that drifts slowly, using aspect2d for aspect-corrected UI."""
        try:
            from direct.showbase import ShowBaseGlobal
            base = ShowBaseGlobal.base
            tex = get_texture("menu_bg")
        except Exception:
            tex = get_texture("white")
            base = None
        try:
            cm = CardMaker("bg")
            cm.setFrame(-1, 1, -1, 1)
            # Use aspect2d for proper aspect ratio correction
            parent_node = base.aspect2d if base and hasattr(base, "aspect2d") else getattr(self.app, "aspect2d", None)
            if parent_node is None:
                parent_node = getattr(self.app, "render2d", None)
            self.bg = parent_node.attachNewNode(cm.generate())
            self.bg.setTexture(tex)
            self.bg.setBin("background", 0)
            self.bg.setDepthWrite(False)
            self.bg.setDepthTest(False)
            # Dark background for high contrast
            self.bg.setColorScale(0.15, 0.15, 0.2, 1)
        except Exception:  # pragma: no cover - skip if Panda3D missing
            self.bg = None

    def setup_top_bar(self) -> None:
        """Create a frosted-glass top bar with player avatar, name, and currencies."""
        try:
            # Frosted-glass effect with higher alpha and subtle tint
            frosted_color = (0.1, 0.1, 0.15, 0.8)
            self.top_bar = DirectFrame(
                frameColor=frosted_color,
                frameSize=(-1.0, 1.0, -0.08, 0.08),
                scale=get_widget_scale(),
            )
            set_widget_pos(self.top_bar, (0, 0, 0.92))
            
            # Player avatar with rounded frame effect - fixed positioning
            try:
                photo = get_player_photo("becca")
            except Exception:
                photo = get_texture("white")
            self.avatar = DirectButton(
                image=photo,
                frameColor=(0.2, 0.2, 0.25, 0.9),
                frameSize=(-0.04, 0.04, -0.04, 0.04),  # Smaller frame size
                scale=get_widget_scale(),
                parent=self.top_bar,
            )
            set_widget_pos(self.avatar, (-0.8, 0, 0))  # Moved right from -0.9
            
            # Player name with reduced text scaling
            DirectLabel(
                text="Player",
                text_fg=(1, 1, 1, 1),
                text_font=None,  # Use default modern font
                frameColor=(0, 0, 0, 0),
                parent=self.top_bar,
                pos=(-0.65, 0, 0),  # Adjusted to follow avatar
                scale=0.9,  # Reduced from 1.2
                text_scale=0.8,  # Additional text scaling
            )
            
            # Currencies with accent highlights - reduced scaling
            DirectLabel(
                text="Gold: 0 | Tickets: 0",
                text_fg=(0.9, 0.9, 1, 1),  # Slight blue tint for currencies
                frameColor=(0, 0, 0, 0),
                parent=self.top_bar,
                pos=(0.3, 0, 0),  # Adjusted position
                scale=0.8,  # Reduced from 1.0
                text_scale=0.8,
            )
            
            # Corner quick-access icons - reduced size
            for icon, pos in [
                ("icon_message_square", (-0.95, 0, 0.85)),
                ("icon_folder_open", (0.95, 0, 0.85)),
            ]:
                img = get_texture(icon)
                btn = DirectButton(
                    image=img, 
                    frameColor=(0.2, 0.2, 0.25, 0.7),
                    frameSize=(-0.025, 0.025, -0.025, 0.025),  # Smaller
                    scale=get_widget_scale() * 0.8,  # Reduced scale
                )
                set_widget_pos(btn, pos)
                self.corner_buttons.append(btn)
        except Exception:  # pragma: no cover - headless tests
            self.top_bar = None
            self.banner = None
            self.avatar = None
            self.corner_buttons = []

    def setup_banner(self) -> None:
        """Create a central banner for events and announcements."""
        try:
            banner_tex = get_texture("menu_bg")
        except Exception:
            banner_tex = get_texture("white")
        
        try:
            self.banner = DirectFrame(
                frameColor=(0.05, 0.05, 0.1, 0.6),
                frameSize=(-0.5, 0.5, -0.1, 0.1),  # Smaller banner
                scale=get_widget_scale(),
            )
            set_widget_pos(self.banner, (0, 0, 0.3))
            
            # Banner content with reduced text scaling
            DirectLabel(
                text="Welcome to Midori AI AutoFighter",
                text_fg=(1, 1, 1, 1),
                frameColor=(0, 0, 0, 0),
                parent=self.banner,
                pos=(0, 0, 0),
                scale=1.0,  # Reduced from 1.5
                text_scale=0.7,  # Additional text scaling reduction
            )
        except Exception:  # pragma: no cover - headless tests
            self.banner = None

    def setup_button_grid(self) -> None:
        """Create a 2x3 high-contrast grid of large Lucide icons anchored near the bottom."""
        buttons = [
            ("New Run", "icon_play", self.new_run),
            ("Load Run", "icon_folder_open", self.load_run),
            ("Edit Player", "icon_user", self.edit_player),
            ("Options", "icon_settings", self.open_options),
            ("Give Feedback", "icon_message_square", self.give_feedback),
            ("Quit", "icon_power", self.app.userExit),
        ]
        
        # Grid configuration for appropriately sized layout
        cols = 2
        rows = 3
        button_scale = get_widget_scale() * 1.2  # Reduced from 2.0 to fix oversized text
        icon_scale = get_widget_scale() * 0.8  # Reduced from 1.2
        
        # Anchor near bottom edge with generous spacing
        x_positions = [-0.3, 0.3]  # Centered columns
        y_base = -0.6  # Higher up from bottom
        y_spacing = 0.2  # Generous vertical spacing
        
        for i, (label, icon_name, cmd) in enumerate(buttons):
            img = get_texture(icon_name)
            
            # High-contrast rounded pill buttons with proper sizing
            button = DirectButton(
                text=label,
                command=cmd,
                scale=button_scale,
                frameColor=(0.15, 0.15, 0.2, 0.9),  # Dark with high contrast
                text_fg=(1, 1, 1, 1),  # Pure white text
                image=img,
                image_scale=icon_scale,
                text_pos=(0, -0.08),  # Position text below icon
                frameSize=(-0.15, 0.15, -0.08, 0.08),  # Adjusted for proper sizing
                text_font=None,  # Modern sans-serif
                text_scale=0.8,  # Add explicit text scaling to reduce size
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
        """Set up the Load Run menu with consistent Arknights-inspired styling."""
        runs = self.available_runs()
        labels = [(label, lambda p=p: self.start_run(p)) for p, label in runs]
        labels.append(("Back", self.back))
        
        # Use consistent styling with main menu
        top = self.BUTTON_SPACING * (len(labels) - 1) / 2
        for i, (text, cmd) in enumerate(labels):
            button = DirectButton(
                text=text,
                command=cmd,
                scale=get_widget_scale() * 1.8,
                frameColor=(0.15, 0.15, 0.2, 0.9),  # Consistent frosted-glass
                text_fg=(1, 1, 1, 1),  # Pure white text
                frameSize=(-0.4, 0.4, -0.04, 0.04),  # Rounded pill shape
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


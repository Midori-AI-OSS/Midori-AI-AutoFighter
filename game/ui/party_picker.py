"""Party picker screen for selecting allies before a run.

This implementation mirrors the layout guidance from the main menu and
introduces a scrollable roster, placeholder 3D preview, and tabbed stats
panel. Each icon sits in a circular slot whose outline color represents the
character's element. Selecting an icon toggles a check mark in its lower-right
corner and adds the character to the party list (up to four members).

The center of the screen displays a simple 3D model that the player can rotate
left or right. The right side hosts a tabbed panel with stat icons so the user
can review details for the highlighted character.
"""

from __future__ import annotations

import random
import subprocess
import tempfile

from pathlib import Path
from typing import get_origin
from typing import get_type_hints
from dataclasses import fields

from PIL import Image
from PIL import ImageDraw

try:  # pragma: no cover - fallbacks for headless tests
    from panda3d.core import NodePath
    from panda3d.core import TextNode
    from direct.gui.DirectFrame import DirectFrame
    from panda3d.core import TransparencyAttrib
    from direct.gui.DirectLabel import DirectLabel
    from direct.gui.DirectButton import DirectButton
    from direct.gui.DirectScrolledFrame import DirectScrolledFrame
except Exception:  # pragma: no cover
    DirectButton = DirectFrame = DirectLabel = DirectScrolledFrame = object  # type: ignore
    NodePath = TextNode = TransparencyAttrib = object  # type: ignore

from game.ui.menu import TopBar
from game.ui.run_map import RunMap
from autofighter.scene import Scene
from autofighter.stats import Stats
from autofighter.save import DB_PATH
from game.ui.menu import TopLeftPanel
from autofighter.gui import set_widget_pos
from autofighter.gui import get_widget_scale

DT_ICONS = {
    "Generic": "assets/textures/icon_circle.png",
    "Light": "assets/textures/icon_sun.png",
    "Dark": "assets/textures/icon_moon.png",
    "Wind": "assets/textures/icon_wind.png",
    "Lightning": "assets/textures/icon_zap.png",
    "Fire": "assets/textures/icon_flame.png",
    "Ice": "assets/textures/icon_snowflake.png",
}

def rebuild_models(model_dir: Path) -> None:
    """Rebuild ``.egg`` models into ``.bam`` every boot.

    Panda3D converts EGG files to BAM for fast loading.  During development we
    regenerate these each time the picker is opened so artists can tweak the
    source meshes without manual steps.  Missing tools or models are ignored so
    tests can run without Panda3D utilities installed.
    """

    for egg in model_dir.glob("*.egg"):
        bam = egg.with_suffix(".bam")
        try:
            if bam.exists():
                bam.unlink()
            subprocess.run(
                ["egg2bam", "-o", str(bam), str(egg)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:  # pragma: no cover - tool may be missing
            continue


def _make_ring(color: tuple[int, int, int], size: int = 64) -> str:
    """Return a temporary image path for a circular ring in ``color``."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, size - 1, size - 1), outline=color, width=6)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(tmp.name)
    return tmp.name


def _mask_icon(path: Path, size: int = 64) -> str:
    """Return a circularly cropped copy of ``path``."""

    img = Image.open(path).convert("RGBA")
    img = img.resize((size, size))
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(tmp.name)
    return tmp.name


class PickerTopLeftPanel(TopLeftPanel):
    """Top-left panel with home, pulls, and crafting buttons."""

    def __init__(self, parent, home_cmd, pull_characters_cmd, craft_items_cmd):
        super().__init__(parent, home_cmd, pull_characters_cmd, craft_items_cmd)
        # Swap the avatar icon for a home button that returns to the menu.
        scale = get_widget_scale() * 0.95
        if hasattr(self.avatar_button, "setScale"):
            self.avatar_button["image"] = "assets/textures/icon_home.png"
            self.avatar_button["command"] = home_cmd
            self.avatar_button.setScale(scale)
        else:  # fallback for dict-like stubs
            self.avatar_button["image"] = "assets/textures/icon_home.png"
            self.avatar_button["command"] = home_cmd
            self.avatar_button["scale"] = scale


class PartyPicker(Scene):
    """Scene for selecting allies before starting a run."""

    def __init__(self, app: object, player: Stats, *, roster: list[str] | None = None) -> None:
        self.app = app
        self.player = player
        self.char_ids = list(roster or [])
        if "player" not in self.char_ids:
            self.char_ids.insert(0, "player")
        self.selected: list[str] = []
        self.root: DirectFrame | None = None
        self.top_left_panel: PickerTopLeftPanel | None = None
        self.top_bar: TopBar | None = None
        self.scroll: DirectScrolledFrame | None = None
        self.buttons: dict[str, DirectButton] = {}
        self.slots: list[DirectFrame] = []
        self.checkmarks: dict[str, DirectLabel] = {}
        self.char_stats: dict[str, Stats] = {}
        self.stat_labels: dict[str, DirectLabel] = {}
        self.stat_icons: dict[str, DirectLabel] = {}
        self.dmg_plugins: dict[str, type] = {}
        self.model: NodePath | None = None
        self.model_name: str | None = None
        self.rotation = 0.0

    # ------------------------------------------------------------------
    # UI setup
    def setup(self) -> None:
        parent = getattr(self.app, "aspect2d", NodePath("party-picker-root"))
        bg_dir = Path("assets/textures/backgrounds")
        choices = list(bg_dir.glob("background_*.png"))
        bg_path = random.choice(choices) if choices else None
        self.root = DirectFrame(
            parent=parent,
            frameSize=(-1, 1, -1, 1),
            image=str(bg_path) if bg_path else None,
            image_scale=1.7,
        )
        self.top_bar = TopBar(self.root, DB_PATH, Path("assets/textures/players"))
        self.top_left_panel = PickerTopLeftPanel(
            self.root,
            self.home,
            self.pull_characters,
            self.craft_items,
        )
        self._layout_buttons()

        # Build roster list inside a vertical scroll frame on the left
        self.scroll = DirectScrolledFrame(
            parent=self.root,
            frameSize=(-0.48, 0.32, -0.9, 0.7),
            canvasSize=(-0.48, 0.32, -0.9 - 0.25 * len(self.char_ids), 0.7),
            pos=(-1.05, 0, 0),
            scrollBarWidth=0,
            relief="flat",
            frameColor=(1, 1, 1, 0),
            manageScrollBars=False,
        )
        try:
            self.scroll.horizontalScroll.destroy()
        except Exception:  # pragma: no cover - stubbed widgets
            pass
        try:
            self.scroll.verticalScroll.setTransparency(TransparencyAttrib.MAlpha)
        except Exception:  # pragma: no cover - stubbed widgets
            pass

        loader = getattr(self.app, "plugin_loader", None)
        self.dmg_plugins = loader.get_plugins("damage_type") if loader else {}
        player_plugins = loader.get_plugins("player") if loader else {}
        icons_dir = Path("assets/textures/players")
        fallback_icons = list((icons_dir / "fallbacks").glob("*.png"))
        for idx, cid in enumerate(self.char_ids):
            if cid == "player":
                icon_path = None
                if self.top_bar:
                    try:
                        icon_path = self.top_bar._ensure_avatar(DB_PATH, icons_dir)
                    except Exception:
                        icon_path = None
                icon = Path(icon_path) if icon_path else icons_dir / "player.png"
                if not icon.exists():
                    icon = Path("assets/textures/icon_user.png")
                char_stats = self.player
            else:
                icon = icons_dir / f"{cid}.png"
                if not icon.exists() and fallback_icons:
                    icon = random.choice(fallback_icons)
                plugin_cls = player_plugins.get(cid)
                char_stats = plugin_cls() if plugin_cls else Stats(hp=1, max_hp=1)
            self.char_stats[cid] = char_stats
            colors: list[tuple[int, int, int]] = []
            icons: list[str] = []
            for dt in getattr(char_stats, "damage_types", []):
                plug = self.dmg_plugins.get(dt)
                if plug:
                    colors.append(plug().color)
                    icons.append(DT_ICONS.get(dt, DT_ICONS["Generic"]))
            if colors:
                choice = random.randrange(len(colors))
                color = colors[choice]
                dmg_icon_path = icons[choice]
            else:
                color = (255, 255, 255)
                dmg_icon_path = DT_ICONS["Generic"]
            slot = DirectFrame(
                parent=self.scroll.getCanvas(),
                frameColor=(1, 1, 1, 0),
                relief="flat",
            )
            slot.setScale(0.11)
            set_widget_pos(slot, (0, 0, 0.55 - idx * 0.25))
            slot.setTransparency(TransparencyAttrib.MAlpha)
            self.slots.append(slot)
            masked_icon = _mask_icon(icon)
            btn = DirectButton(
                parent=slot,
                image=str(masked_icon),
                relief="flat",
                command=self.select,
                extraArgs=[cid],
            )
            btn["frameColor"] = (1, 1, 1, 0)
            btn["sortOrder"] = 0
            btn.setTransparency(TransparencyAttrib.MAlpha)
            for state in ("image0", "image1", "image2", "image3"):
                try:
                    node = btn.component(state)
                except Exception:
                    node = None
                if node:
                    node.setTransparency(TransparencyAttrib.MAlpha)
            ring_path = _make_ring(color)
            ring = DirectFrame(
                parent=slot,
                image=ring_path,
                frameColor=(1, 1, 1, 0),
                relief="flat",
            )
            ring["state"] = "disabled"
            ring["sortOrder"] = 1
            ring.setTransparency(TransparencyAttrib.MAlpha)
            dmg_icon = DirectFrame(
                parent=slot,
                image=dmg_icon_path,
                frameColor=(1, 1, 1, 0),
                relief="flat",
                pos=(-0.08, 0, 0.08),
                scale=0.04,
            )
            dmg_icon["state"] = "disabled"
            dmg_icon["sortOrder"] = 2
            dmg_icon.setTransparency(TransparencyAttrib.MAlpha)
            if cid != "player":
                mark = DirectLabel(
                    parent=slot,
                    image="assets/textures/icon_diamond.png",
                    image_color=(0, 1, 0, 1),
                    relief="flat",
                    pos=(0.07, 0, -0.07),
                    scale=0.05,
                )
                mark["state"] = "disabled"
                mark["sortOrder"] = 3
                mark.hide()
                self.checkmarks[cid] = mark
            self.buttons[cid] = btn

        # Fade textures at top and bottom to soften the roster edges
        top_fade = DirectFrame(
            parent=self.root,
            image="assets/textures/roster_fade_top.png",
            frameColor=(1, 1, 1, 0),
            pos=(-1.05, 0, 0.7),
            scale=(0.25, 1, 0.05),
        )
        top_fade.setTransparency(TransparencyAttrib.MAlpha)
        bottom_fade = DirectFrame(
            parent=self.root,
            image="assets/textures/roster_fade_bottom.png",
            frameColor=(1, 1, 1, 0),
            pos=(-1.05, 0, -0.7),
            scale=(0.25, 1, 0.05),
        )
        bottom_fade.setTransparency(TransparencyAttrib.MAlpha)

        # Tabbed stats panel on the right
        self._build_stat_panel()

        # Load the player's model preview and enable rotation
        self.show_body(self.player)
        if hasattr(self.app, "accept"):
            self.app.accept("arrow_left", self.rotate_model, [-10])
            self.app.accept("arrow_right", self.rotate_model, [10])

        self.start_button = DirectButton(
            parent=self.root,
            text="Start Run",
            scale=get_widget_scale(),
            command=self.start_run,
            frameColor=(1, 1, 1, 0.3),
            relief="flat",
        )
        set_widget_pos(self.start_button, (0.8, 0, -0.8))

    # ------------------------------------------------------------------
    def _layout_buttons(self) -> None:
        if not self.top_left_panel:
            return
        start_x = 0.01 * 12
        spacing = 0.25
        z = -0.085
        for i, button in enumerate(self.top_left_panel.buttons):
            set_widget_pos(button, (start_x + i * spacing, 0, z))

    # ------------------------------------------------------------------
    def _build_stat_panel(self) -> None:
        """Create a simple tabbed stats viewer."""

        panel = DirectFrame(
            parent=self.root,
            frameSize=(0, 0.6, -0.6, 0.6),
            frameColor=(0, 0, 0, 0.2),
            pos=(0.7, 0, 0),
        )
        self.stat_tabs = {}

        groups: dict[str, list[str]] = {"Numbers": [], "Flags": [], "Lists": []}
        hints = get_type_hints(Stats)
        for field in fields(Stats):
            ftype = hints.get(field.name, field.type)
            origin = get_origin(ftype)
            if ftype in (int, float):
                groups["Numbers"].append(field.name)
            elif ftype is bool:
                groups["Flags"].append(field.name)
            elif origin is list:
                groups["Lists"].append(field.name)

        groups = {k: v for k, v in groups.items() if v}

        for idx, (name, stats) in enumerate(groups.items()):
            btn = DirectButton(
                parent=panel,
                text=name,
                pos=(0.3, 0, 0.5 - idx * 0.1),
                command=self.show_tab,
                extraArgs=[name],
            )
            btn.setScale(0.05)
            tab_frame = DirectFrame(parent=panel, frameColor=(0, 0, 0, 0))
            for s_idx, stat in enumerate(stats):
                icon = DirectLabel(
                    parent=tab_frame,
                    image="assets/textures/icon_diamond.png",
                    relief="flat",
                    pos=(0, 0, 0.3 - s_idx * 0.1),
                    scale=0.05,
                )
                label = DirectLabel(
                    parent=tab_frame,
                    text="",
                    text_align=TextNode.ALeft,
                    pos=(0.1, 0, 0.3 - s_idx * 0.1),
                    scale=0.05,
                )
                self.stat_icons[stat] = icon
                self.stat_labels[stat] = label
            tab_frame.hide()
            self.stat_tabs[name] = tab_frame

        self.damage_buttons: dict[str, DirectButton] = {}
        for idx, dtype in enumerate(sorted(self.dmg_plugins)):
            icon = DT_ICONS.get(dtype, DT_ICONS["Generic"])
            btn = DirectButton(
                parent=panel,
                image=icon,
                relief="flat",
                command=self.set_damage_type,
                extraArgs=[dtype],
            )
            btn.setScale(0.05)
            set_widget_pos(btn, (0.1 + idx * 0.1, 0, -0.5))
            self.damage_buttons[dtype] = btn

        self.stat_panel = panel
        if groups:
            first = next(iter(groups))
            self.show_tab(first)
        self.show_stats(self.player)

    # ------------------------------------------------------------------
    def show_tab(self, name: str) -> None:
        for frame in self.stat_tabs.values():
            frame.hide()
        if name in self.stat_tabs:
            self.stat_tabs[name].show()

    def show_stats(self, stats: Stats) -> None:
        for stat, label in self.stat_labels.items():
            value = getattr(stats, stat, 0)
            icon = self.stat_icons.get(stat)
            if icon:
                icon["image"] = "assets/textures/icon_diamond.png"
            label["text_fg"] = (1, 1, 1, 1)
            if isinstance(value, str) and value in self.dmg_plugins:
                if icon:
                    icon["image"] = DT_ICONS.get(value, DT_ICONS["Generic"])
                r, g, b = self.dmg_plugins[value]().color
                label["text_fg"] = (r / 255, g / 255, b / 255, 1)
            label["text"] = f"{stat}: {value}"

    def show_body(self, stats: Stats) -> None:
        """Display the body model for ``stats`` based on its ``char_type``."""

        loader = getattr(self.app, "loader", None)
        render = getattr(self.app, "render", None)
        model_dir = Path("assets/models")
        rebuild_models(model_dir)
        model_name = f"body_{getattr(stats.char_type, 'value', 'a').lower()}"
        if not (loader and render):
            self.model_name = model_name
            return
        model = None
        for ext in (".bam", ".egg"):
            try:
                model = loader.loadModel(str(model_dir / f"{model_name}{ext}"))
                break
            except Exception:  # pragma: no cover - missing asset
                continue
        if model is None:
            try:
                model = loader.loadModel("models/box")
                model_name = "models/box"
            except Exception:
                return

        if self.model:
            try:
                self.model.removeNode()
            except Exception:  # pragma: no cover - safe cleanup
                pass

        self.model = model
        self.model_name = model_name
        try:
            self.model.reparentTo(render)
            self.model.setPos(0, 5, 0)
        except Exception:  # pragma: no cover - render missing
            pass

    def set_damage_type(self, dtype: str) -> None:
        self.player.base_damage_type = dtype
        self.player.damage_types = [dtype]
        self.show_stats(self.player)

    # ------------------------------------------------------------------
    def rotate_model(self, delta: float) -> None:
        if self.model:
            self.rotation += delta
            try:
                self.model.setH(self.rotation)
            except Exception:  # pragma: no cover - model may be stub
                pass

    # ------------------------------------------------------------------
    # Selection logic
    def toggle(self, char_id: str) -> None:
        mark = self.checkmarks.get(char_id)
        if char_id in self.selected:
            self.selected.remove(char_id)
            if mark:
                mark.hide()
        elif len(self.selected) < 4:
            self.selected.append(char_id)
            if mark:
                mark.show()

    def select(self, char_id: str) -> None:
        if char_id != "player":
            self.toggle(char_id)
            stats = self.char_stats.get(char_id)
            if stats:
                self.show_stats(stats)
                self.show_body(stats)
        else:
            if self.player.max_hp <= 1:
                self.home()
                main_menu = getattr(self.app, "main_menu", None)
                if main_menu and hasattr(main_menu, "edit_player"):
                    try:
                        main_menu.edit_player()
                    except Exception:  # pragma: no cover - stub
                        pass
            else:
                self.show_stats(self.player)
                self.show_body(self.player)

    def start_run(self) -> None:
        if self.app is None:  # pragma: no cover - safeguard
            return
        run_map = RunMap(self.app, self.player, self.selected, DB_PATH)
        self.app.scene_manager.switch_to(run_map)  # type: ignore[attr-defined]

    def home(self) -> None:
        if self.app is None:  # pragma: no cover
            return
        # Tear down the picker scene and reveal the main menu again
        try:
            self.app.scene_manager.switch_to(None)  # type: ignore[attr-defined]
        except Exception:
            pass
        main_menu = getattr(self.app, "main_menu", None)
        if main_menu:
            try:
                main_menu.show()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Stub commands
    def pull_characters(self) -> None:  # pragma: no cover - placeholders
        """Placeholder for character pulls."""

    def craft_items(self) -> None:  # pragma: no cover - placeholders
        """Placeholder for crafting."""

    # ------------------------------------------------------------------
    def teardown(self) -> None:
        for btn in self.buttons.values():
            try:
                btn.destroy()
            except Exception:
                pass
        for mark in self.checkmarks.values():
            try:
                mark.destroy()
            except Exception:
                pass
        for slot in self.slots:
            try:
                slot.destroy()
            except Exception:
                pass
        self.buttons.clear()
        self.checkmarks.clear()
        self.slots.clear()
        if self.scroll:
            try:
                self.scroll.destroy()
            except Exception:
                pass
            self.scroll = None
        if self.top_left_panel:
            for btn in self.top_left_panel.buttons:
                try:
                    btn.destroy()
                except Exception:
                    pass
            self.top_left_panel = None
        if self.top_bar:
            try:
                self.top_bar.frame.destroy()
            except Exception:
                pass
            self.top_bar = None
        if hasattr(self.app, "ignore"):
            self.app.ignore("arrow_left")
            self.app.ignore("arrow_right")
        if self.model:
            try:
                self.model.removeNode()
            except Exception:
                pass
            self.model = None
        if hasattr(self, "start_button") and self.start_button:
            try:
                self.start_button.destroy()
            except Exception:
                pass
            self.start_button = None
        if self.root:
            try:
                self.root.destroy()
            except Exception:
                pass
            self.root = None


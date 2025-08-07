from __future__ import annotations

from pathlib import Path

try:
    from direct.gui.DirectGui import DirectButton
    from direct.gui.DirectGui import DirectCheckButton
    from direct.gui.DirectGui import DirectLabel
    from direct.showbase.ShowBase import ShowBase
except Exception:  # pragma: no cover - fallback for headless tests
    class _Widget:
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
        pass

    class DirectLabel(_Widget):  # type: ignore[dead-code]
        pass

    class ShowBase:  # type: ignore[dead-code]
        pass

from .run_map import RunMap
from game.actors import CharacterType
from autofighter.gui import FRAME_COLOR
from autofighter.gui import TEXT_COLOR
from autofighter.gui import get_widget_scale
from autofighter.gui import set_widget_pos
from autofighter.save import load_roster
from autofighter.scene import Scene
from autofighter.stats import Stats
from plugins.plugin_loader import PluginLoader


class PartyPicker(Scene):
    MAX_ALLIES = 4
    BUTTON_SPACING = 0.2

    def __init__(
        self,
        app: ShowBase,
        player: Stats,
        seed_store_path: Path | None = None,
        roster: list[str] | None = None,
    ) -> None:
        self.app = app
        self.player = player
        self.seed_store_path = seed_store_path
        self.roster = roster if roster is not None else load_roster()
        self.checks: list[DirectCheckButton] = []
        self.labels: list[DirectLabel] = []
        self.selected: set[str] = set()
        self.char_ids: list[str] = []

    def available_characters(self) -> list[tuple[str, str, CharacterType]]:
        loader = PluginLoader()
        loader.discover("plugins/players")
        players = loader.get_plugins("player")
        owned = set(self.roster)
        return [
            (pid, cls.name, getattr(cls, "char_type", CharacterType.C))
            for pid, cls in players.items()
            if pid in owned
        ]

    def setup(self) -> None:
        chars = self.available_characters()
        self.char_ids = [pid for pid, _name, _type in chars]
        top = self.BUTTON_SPACING * (len(chars) - 1) / 2
        for i, (pid, name, ctype) in enumerate(chars):
            label = f"{name} ({ctype.name})"
            check = DirectCheckButton(
                text=label,
                text_fg=TEXT_COLOR,
                frameColor=FRAME_COLOR,
                scale=get_widget_scale(),
                command=self.toggle,
                extraArgs=[pid],
            )
            set_widget_pos(check, (0, 0, top - i * self.BUTTON_SPACING))
            self.checks.append(check)
        start = DirectButton(
            text="Start",
            text_fg=TEXT_COLOR,
            frameColor=FRAME_COLOR,
            scale=get_widget_scale(),
            command=self.start_run,
        )
        set_widget_pos(start, (0, 0, top - len(chars) * self.BUTTON_SPACING))
        self.labels.append(start)
        self.app.accept("escape", self.back)

    def teardown(self) -> None:
        for widget in self.checks + self.labels:
            widget.destroy()
        self.checks.clear()
        self.labels.clear()
        self.app.ignore("escape")

    def toggle(self, pid: str, *_: object) -> None:
        if pid in self.selected:
            self.selected.remove(pid)
            return
        if len(self.selected) >= self.MAX_ALLIES:
            return
        self.selected.add(pid)

    def start_run(self) -> None:
        party = list(self.selected)
        self.app.scene_manager.switch_to(
            RunMap(self.app, self.player, party, self.seed_store_path)
        )

    def back(self) -> None:
        from .menu import MainMenu

        self.app.scene_manager.switch_to(MainMenu(self.app))

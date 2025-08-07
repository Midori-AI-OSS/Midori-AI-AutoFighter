from __future__ import annotations

import random
from pathlib import Path

try:
    from direct.gui.DirectGui import DirectButton
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

        def bind(self, *_args: object, **_kwargs: object) -> None:
            pass

    class DirectButton(_Widget):  # type: ignore[dead-code]
        pass

    class DirectLabel(_Widget):  # type: ignore[dead-code]
        pass

    class ShowBase:  # type: ignore[dead-code]
        pass

from autofighter.gui import FRAME_COLOR
from autofighter.gui import TEXT_COLOR
from autofighter.gui import get_widget_scale
from autofighter.gui import set_widget_pos
from autofighter.scene import Scene
from autofighter.stats import Stats
from autofighter.map_generation import MapGenerator
from autofighter.map_generation import render_floor


class RunMap(Scene):
    def __init__(
        self,
        app: ShowBase,
        player: Stats,
        party: list[str] | None = None,
        seed_store_path: Path | None = None,
    ) -> None:
        self.app = app
        self.player = player
        self.party = party or []
        self.seed_store_path = seed_store_path
        self.label: DirectLabel | None = None

    def setup(self) -> None:
        generator = MapGenerator(
            random.randint(0, 999_999),
            seed_store_path=self.seed_store_path,
        )
        nodes = generator.generate_floor(1)
        text = render_floor(nodes)
        self.label = DirectLabel(
            text=text,
            text_fg=TEXT_COLOR,
            frameColor=FRAME_COLOR,
            scale=get_widget_scale(),
        )
        set_widget_pos(self.label, (0, 0, 0))
        self.app.accept("enter", self.enter_first_room)
        self.app.accept("escape", self.back)

    def teardown(self) -> None:
        if self.label:
            self.label.destroy()
            self.label = None
        self.app.ignore("enter")
        self.app.ignore("escape")

    def enter_first_room(self) -> None:
        from autofighter.battle_room import BattleRoom  # local import to defer Panda3D dependency

        battle = BattleRoom(
            self.app,
            return_scene_factory=lambda: RunMap(
                self.app,
                self.player,
                self.party,
                self.seed_store_path,
            ),
            player=self.player,
            party=self.party,
        )
        self.app.scene_manager.switch_to(battle)

    def back(self) -> None:
        from .menu import MainMenu

        self.app.scene_manager.switch_to(MainMenu(self.app))

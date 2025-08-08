"""Minimal run map scene.

Displays a placeholder map and enters a battle room when the first
room is selected.
"""

from __future__ import annotations

from pathlib import Path

from direct.gui.DirectGui import DirectLabel

from autofighter.scene import Scene
from autofighter.stats import Stats


class RunMap(Scene):
    """Simple scene showing placeholder map text."""

    def __init__(
        self,
        app: object,
        player: Stats,
        party: list[str],
        seed_store_path: Path,
    ) -> None:
        self.app = app
        self.player = player
        self.party = party
        self.seed_store_path = Path(seed_store_path)
        self.label: DirectLabel | None = None

    def setup(self) -> None:
        self.label = DirectLabel(text="00: -> 01,02,03")

    def enter_first_room(self) -> None:
        from autofighter.battle_room import BattleRoom

        battle = BattleRoom(player=self.player, party=self.party)
        self.app.scene_manager.switch_to(battle)

    def teardown(self) -> None:
        if self.label:
            self.label.destroy()
            self.label = None

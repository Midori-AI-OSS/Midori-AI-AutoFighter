"""Example healing-over-time plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from plugins.hots.base import HotPlugin

if TYPE_CHECKING:
    from player import Player


class Regeneration(HotPlugin):
    """Heals targets gradually over time.

    Attributes
    ----------
    plugin_type: str
        Category consumed by the plugin loader.
    id: str
        Unique identifier used to select this plugin.
    name: str
        Display name shown to the user.
    """

    plugin_type = "hot"
    id = "regeneration"
    name = "Regeneration"

    def __init__(self, healing: float = 5, turns: int = 3) -> None:
        self.healing = healing
        self.turns = turns

    def tick(self, target: Player, dt: int = 1) -> bool:
        """Heal ``target`` over ``dt`` ticks.

        Returns ``True`` while the effect remains active.
        """
        if self.turns <= 0:
            return False
        target.HP = min(target.MHP, target.HP + self.healing * dt)
        self.turns -= dt
        return self.turns > 0

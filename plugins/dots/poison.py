"""Example damage-over-time plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class Poison:
    """Inflicts poison damage each tick.

    Attributes
    ----------
    plugin_type: str
        Category consumed by the plugin loader.
    id: str
        Unique identifier used to select this plugin.
    name: str
        Display name shown to the user.
    """

    plugin_type = "dot"
    id = "poison"  # Unique identifier used by the game
    name = "Poison"  # Display name

    def __init__(self, damage: float = 5, turns: int = 3) -> None:
        self.damage = damage
        self.turns = turns

    def tick(self, target: Player, dt: int = 1) -> bool:
        """Apply poison damage to ``target`` over ``dt`` ticks.

        Returns ``True`` while the effect remains active.
        """
        if self.turns <= 0:
            return False
        target.HP -= self.damage * dt
        self.turns -= dt
        return self.turns > 0

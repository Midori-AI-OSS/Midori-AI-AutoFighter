"""Template for creating a damage-over-time (DoT) plugin.

Fill out the TODOs to apply ongoing damage to targets.
"""


from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class DotPlugin:
    """Example DoT plugin skeleton."""

    plugin_type = "dot"
    id = "example_dot"  # Unique identifier used by the game
    name = "Example DoT"  # Display name

    def __init__(self, damage: float = 5, turns: int = 3) -> None:
        self.damage = damage
        self.turns = turns

    def tick(self, target: Player, dt: int = 1) -> bool:
        """Apply damage to ``target`` over ``dt`` ticks.

        Returns ``True`` while the effect remains active.
        Customize damage and duration in subclasses.
        """

        if self.turns <= 0:
            return False
        target.HP -= self.damage * dt
        self.turns -= dt
        return self.turns > 0

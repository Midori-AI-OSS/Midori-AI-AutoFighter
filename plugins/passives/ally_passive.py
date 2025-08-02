"""Ally-specific passive effect.

This passive applies only to the player version of Ally and differs from any
foe modifiers in :mod:`foe_passive_builder`.
"""

from __future__ import annotations

from plugins.passives.base import PassivePlugin


class AllyPassive(PassivePlugin):
    """Boost Ally's stats and reduce dodge."""

    plugin_type = "passive"
    id = "ally_passive"
    name = "Ally Passive"

    def __init__(self) -> None:
        super().__init__(self.name)

    def on_apply(self, player) -> None:
        """Apply Ally's unique stat modifiers."""
        player.Atk = int(player.Atk * 1.5)
        player.Def = int(player.Def * 1.5)
        player.CritDamageMod *= (0.005 * player.level) + 1
        player.DodgeOdds /= 1000

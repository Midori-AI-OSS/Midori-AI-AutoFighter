"""Luna-specific passive effect.

This passive applies only to the player version of Luna and mirrors the
bonuses foes receive in :mod:`foe_passive_builder`.
"""

from __future__ import annotations

from plugins.passives.base import PassivePlugin


class LunaPassive(PassivePlugin):
    """Reduce max HP for evasion and boost defense."""

    plugin_type = "passive"
    id = "luna_passive"
    name = "Luna Passive"

    def __init__(self) -> None:
        super().__init__(self.name)

    def on_apply(self, player) -> None:
        """Apply Luna's unique stat modifiers."""
        dodge_buff = 0.35
        max_hp_debuff = player.MHP / 4

        while player.MHP > max_hp_debuff:
            dodge_buff += 0.001 * player.Vitality
            player.MHP -= 1

        player.Atk = int(player.Atk * 1)
        player.Def = int(player.Def * 2)
        player.gain_crit_rate(0.00001 * player.level)
        player.DodgeOdds += dodge_buff * player.Vitality


from __future__ import annotations

import random

from plugins.passives.base import PassivePlugin


class CarlyPassive(PassivePlugin):
    """Rebalance Carly's stats toward defense.

    Foe-only bonuses remain in :mod:`foe_passive_builder`.
    """

    plugin_type = "passive"
    id = "carly_passive"
    name = "Carly Passive"

    def __init__(self) -> None:
        super().__init__(self.name)

    def on_apply(self, player) -> None:  # noqa: D401
        """Shift attack into defense and grant a defensive blessing."""
        max_atk_stat = 0
        item_buff = 0.0
        def_to_add = 0
        if player.Items:
            def_to_add = (
                player.check_base_stats(player.Def, player.Items[0].power / 2)
                + (player.Atk // 2)
            )
        while player.Atk > max_atk_stat:
            player.Def += player.check_base_stats(player.Def, def_to_add)
            player.Atk -= 1
        while player.Regain > 5:
            player.Def += player.check_base_stats(player.Def, def_to_add)
            player.Regain -= 0.001
        player.Atk = int(player.Atk) + 1
        player.Def += player.check_base_stats(
            player.Def, int(player.Def * player.level) + 1
        )
        player.gain_crit_damage(0.0002 * player.level)
        while player.Def > 25000:
            item_buff += random.uniform(0.05, 0.25)
            player.Def -= 5
        for item in player.Items:
            item.name = "Carly's Blessing of Defense"
            item.power += player.level * item_buff


from __future__ import annotations

from plugins.passives.base import PassivePlugin


class BubblesPassive(PassivePlugin):
    """Enhance Bubbles's items for player-controlled versions.

    Foe-specific bonuses remain in :mod:`foe_passive_builder`.
    """

    plugin_type = "passive"
    id = "bubbles_passive"
    name = "Bubbles Passive"

    def __init__(self) -> None:
        super().__init__(self.name)

    def on_apply(self, player) -> None:  # noqa: D401
        """Rename items and boost their power."""
        for item in player.Items:
            item.name = "Bubbles's Blessing of Damage, Defense, and Utility"
            item.power += player.level * 0.0003

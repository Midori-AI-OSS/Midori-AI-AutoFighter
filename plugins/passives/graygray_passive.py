from __future__ import annotations

from plugins.passives.base import PassivePlugin


class GraygrayPassive(PassivePlugin):
    """Player-only Regain scaling for Graygray.

    Foe versions rely on separate logic in :mod:`foe_passive_builder`.
    """

    plugin_type = "passive"
    id = "graygray_passive"
    name = "Graygray Passive"

    def __init__(self) -> None:
        super().__init__(self.name)

    def on_apply(self, player) -> None:
        """Adjust ``player.Regain`` by level."""
        player.Regain *= 0.05 * player.level


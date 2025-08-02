"""Example passive plugin."""

from __future__ import annotations

from plugins.passives.base import PassivePlugin


class BleedingBlow(PassivePlugin):
    """Adds a chance to inflict bleeding on attacks."""

    plugin_type = "passive"
    id = "bleeding_blow"
    name = "Bleeding Blow"

    def __init__(self) -> None:
        super().__init__(self.name)

    def on_apply(self, player) -> None:
        """Grant the bleeding effect to ``player``."""

        player.BleedChance += 0.25

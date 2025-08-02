"""Example weapon plugin."""

from player import Player
from plugins.weapons.base import WeaponPlugin


class Sword(WeaponPlugin):
    """Standard sword attack."""

    plugin_type = "weapon"
    id = "sword"  # Unique identifier used by the game
    name = "Sword"  # Display name

    def attack(self, attacker: Player, target: Player) -> float:
        """Deal damage from ``attacker`` to ``target``."""

        damage = attacker.deal_damage(1, target.Type)
        target.take_damage(1, damage)

        return damage


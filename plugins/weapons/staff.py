"""Staff weapon plugin."""

from player import Player
from plugins.weapons.base import WeaponPlugin


class Staff(WeaponPlugin):
    """Magical staff attack."""

    plugin_type = "weapon"
    id = "staff"
    name = "Staff"

    def attack(self, attacker: Player, target: Player) -> float:
        """Deal damage from ``attacker`` to ``target``."""

        damage = attacker.deal_damage(1, target.Type)
        target.take_damage(1, damage)

        return damage


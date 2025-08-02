"""Template for creating a weapon plugin.

Implement attack logic inside :func:`attack`.
"""

from player import Player


class WeaponPlugin:
    """Example weapon plugin skeleton.

    Replace ``id``, ``name``, and ``attack`` with your weapon's details.
    """

    plugin_type = "weapon"
    id = "example_weapon"  # Unique identifier used by the game
    name = "Example Weapon"  # Display name shown to players

    def attack(self, attacker: Player, target: Player) -> float:
        """Apply damage from ``attacker`` to ``target``.

        Adjust the damage modifier or type to fit your weapon.
        """

        damage = attacker.deal_damage(1, target.Type)
        target.take_damage(1, damage)

        return damage

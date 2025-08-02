"""Template for creating a weapon plugin.

Implement attack logic inside :func:`attack`.
"""


class WeaponPlugin:
    """Example weapon plugin skeleton."""

    plugin_type = "weapon"
    id = "TODO_unique_id"  # TODO: unique identifier used by the game
    name = "TODO name"  # TODO: display name

    def attack(self, attacker, target):
        """TODO: apply damage from ``attacker`` to ``target``."""
        raise NotImplementedError

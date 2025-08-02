"""Example weapon plugin."""


class Sword:
    """Standard sword attack.

    Attributes
    ----------
    plugin_type: str
        Category consumed by the plugin loader.
    id: str
        Unique identifier used to select this plugin.
    name: str
        Display name shown to the user.
    """

    plugin_type = "weapon"
    id = "sword"  # Unique identifier used by the game
    name = "Sword"  # Display name

    def attack(self, attacker, target):
        """Deal damage from ``attacker`` to ``target``.

        Called each time the weapon is used.
        """
        # TODO: implement damage application
        raise NotImplementedError

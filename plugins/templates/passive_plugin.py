"""Template for creating a passive plugin.

Implement stat modifiers or other effects in :func:`apply`.
"""


class PassivePlugin:
    """Example passive plugin skeleton."""

    plugin_type = "passive"
    id = "example_passive"  # Unique identifier used by the game
    name = "Example Passive"  # Display name shown in menus

    def apply(self, player):
        """Modify ``player`` in place when the passive is applied.

        Adjust stats or add effects directly to ``player`` here.
        Remove or replace the sample logic below in real implementations.
        """

        player.Defense += 1  # Example: increase player's defense

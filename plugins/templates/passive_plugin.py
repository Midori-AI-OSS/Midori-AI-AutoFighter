"""Template for creating a passive plugin.

Implement stat modifiers or other effects in :func:`apply`.
"""


class PassivePlugin:
    """Example passive plugin skeleton."""

    plugin_type = "passive"
    id = "TODO_unique_id"  # TODO: unique identifier used by the game
    name = "TODO name"  # TODO: display name

    def apply(self, player):
        """TODO: modify ``player`` in place."""
        raise NotImplementedError

"""Template for creating a damage-over-time (DoT) plugin.

Fill out the TODOs to apply ongoing damage to targets.
"""


class DotPlugin:
    """Example DoT plugin skeleton."""

    plugin_type = "dot"
    id = "TODO_unique_id"  # TODO: unique identifier used by the game
    name = "TODO name"  # TODO: display name

    def tick(self, target, dt):
        """TODO: apply damage to ``target`` over ``dt`` seconds."""
        raise NotImplementedError

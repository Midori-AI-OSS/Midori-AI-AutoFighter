"""Template for creating a healing-over-time (HoT) plugin.

Add logic to steadily restore health to targets.
"""


class HotPlugin:
    """Example HoT plugin skeleton."""

    plugin_type = "hot"
    id = "TODO_unique_id"  # TODO: unique identifier used by the game
    name = "TODO name"  # TODO: display name

    def tick(self, target, dt):
        """TODO: heal ``target`` over ``dt`` seconds."""
        raise NotImplementedError

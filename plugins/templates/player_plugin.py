"""Template for creating a player plugin.

Replace example values and logic with your own implementation.
"""

from player import Player


class PlayerPlugin:
    """Example player plugin skeleton.

    Replace ``id``, ``name``, and ``build`` with your player's details.
    """

    plugin_type = "player"
    id = "example_player"  # Unique identifier used by the game
    name = "Example Player"  # Display name shown to players

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Create and return a new :class:`Player` instance.

        Parameters
        ----------
        name:
            Optional display name. Default uses ``self.name``.
        """

        player = Player(name or self.name)
        player.load()  # Load past life stats if available
        player.set_photo(self.id)
        player.isplayer = True
        return player


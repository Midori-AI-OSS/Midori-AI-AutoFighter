"""Player plugin for Lady Darkness."""

from player import Player
from plugins.players.base import PlayerPlugin



class LadyDarkness(PlayerPlugin):
    """Lady Darkness player implementation."""

    plugin_type = "player"
    id = "lady_darkness"
    name = "Lady Darkness"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        return player

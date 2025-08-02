"""Player plugin for Chibi."""

from player import Player
from plugins.players.base import PlayerPlugin



class Chibi(PlayerPlugin):
    """Chibi player implementation."""

    plugin_type = "player"
    id = "chibi"
    name = "Chibi"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        return player

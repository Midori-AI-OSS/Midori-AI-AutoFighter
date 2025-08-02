"""Player plugin for Mimic."""

from player import Player
from plugins.players.base import PlayerPlugin



class Mimic(PlayerPlugin):
    """Mimic player implementation."""

    plugin_type = "player"
    id = "mimic"
    name = "Mimic"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        return player

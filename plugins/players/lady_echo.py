"""Player plugin for Lady Echo."""

from player import Player
from plugins.players.base import PlayerPlugin



class LadyEcho(PlayerPlugin):
    """Lady Echo player implementation."""

    plugin_type = "player"
    id = "lady_echo"
    name = "Lady Echo"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        return player

"""Player plugin for Lady Light."""

from player import Player
from plugins.players.base import PlayerPlugin



class LadyLight(PlayerPlugin):
    """Lady Light player implementation."""

    plugin_type = "player"
    id = "lady_light"
    name = "Lady Light"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        return player

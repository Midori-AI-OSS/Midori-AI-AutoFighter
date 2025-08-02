"""Player plugin for Lady Fire And Ice."""

from player import Player
from plugins.players.base import PlayerPlugin



class LadyFireAndIce(PlayerPlugin):
    """Lady Fire And Ice player implementation."""

    plugin_type = "player"
    id = "lady_fire_and_ice"
    name = "Lady Fire And Ice"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        return player

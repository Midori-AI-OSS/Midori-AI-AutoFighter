"""Player plugin for Luna."""

from player import Player
from passives import get_passive
from plugins.players.base import PlayerPlugin

class Luna(PlayerPlugin):
    """Luna player implementation."""

    plugin_type = "player"
    id = "luna"
    name = "Luna"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        passive = get_passive("luna_passive")
        if passive:
            passive.on_apply(player)
        return player

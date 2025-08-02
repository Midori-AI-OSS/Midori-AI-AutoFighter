"""Example player plugin used as reference."""

from player import Player
from plugins.players.base import PlayerPlugin



class Warrior(PlayerPlugin):
    """Default warrior player."""

    plugin_type = "player"
    id = "warrior"
    name = "Warrior"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        return player

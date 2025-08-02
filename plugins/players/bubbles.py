"""Player plugin for Bubbles."""

from items import ItemType
from player import Player
from passives import get_passive
from plugins.players.base import PlayerPlugin



class Bubbles(PlayerPlugin):
    """Bubbles player implementation."""

    plugin_type = "player"
    id = "bubbles"
    name = "Bubbles"

    def build(self, name: str | None = None, **kwargs) -> Player:
        """Construct and return the player instance."""
        player = Player(name or self.name)
        player.load()
        player.set_photo(self.id)
        player.isplayer = True
        player.Items.append(ItemType())
        passive = get_passive("bubbles_passive")
        if passive:
            passive.on_apply(player)
        return player

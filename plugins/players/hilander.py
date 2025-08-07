from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Hilander:
    plugin_type = "player"
    id = "hilander"
    name = "Hilander"
    char_type = CharacterType.A

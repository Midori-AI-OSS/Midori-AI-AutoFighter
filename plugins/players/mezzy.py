from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Mezzy:
    plugin_type = "player"
    id = "mezzy"
    name = "Mezzy"
    char_type = CharacterType.B

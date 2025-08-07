from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Ally:
    plugin_type = "player"
    id = "ally"
    name = "Ally"
    char_type = CharacterType.B

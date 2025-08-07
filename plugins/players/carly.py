from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Carly:
    plugin_type = "player"
    id = "carly"
    name = "Carly"
    char_type = CharacterType.B

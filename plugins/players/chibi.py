from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Chibi:
    plugin_type = "player"
    id = "chibi"
    name = "Chibi"
    char_type = CharacterType.A

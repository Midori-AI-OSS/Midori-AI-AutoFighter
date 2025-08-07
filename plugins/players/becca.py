from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Becca:
    plugin_type = "player"
    id = "becca"
    name = "Becca"
    char_type = CharacterType.B

from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class LadyOfFire:
    plugin_type = "player"
    id = "lady_of_fire"
    name = "LadyOfFire"
    char_type = CharacterType.B

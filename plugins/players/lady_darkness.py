from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class LadyDarkness:
    plugin_type = "player"
    id = "lady_darkness"
    name = "LadyDarkness"
    char_type = CharacterType.B

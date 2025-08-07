from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class LadyEcho:
    plugin_type = "player"
    id = "lady_echo"
    name = "LadyEcho"
    char_type = CharacterType.B

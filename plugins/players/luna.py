from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Luna:
    plugin_type = "player"
    id = "luna"
    name = "Luna"
    char_type = CharacterType.B

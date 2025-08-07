from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class LadyLight:
    plugin_type = "player"
    id = "lady_light"
    name = "LadyLight"
    char_type = CharacterType.B

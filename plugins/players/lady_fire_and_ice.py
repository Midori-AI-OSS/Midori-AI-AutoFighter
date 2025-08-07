from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class LadyFireAndIce:
    plugin_type = "player"
    id = "lady_fire_and_ice"
    name = "LadyFireAndIce"
    char_type = CharacterType.B

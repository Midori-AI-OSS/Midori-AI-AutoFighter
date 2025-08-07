from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Mimic:
    plugin_type = "player"
    id = "mimic"
    name = "Mimic"
    char_type = CharacterType.C

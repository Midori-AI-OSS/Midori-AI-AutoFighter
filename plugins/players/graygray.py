from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Graygray:
    plugin_type = "player"
    id = "graygray"
    name = "Graygray"
    char_type = CharacterType.B

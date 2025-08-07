from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Bubbles:
    plugin_type = "player"
    id = "bubbles"
    name = "Bubbles"
    char_type = CharacterType.A

from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class Kboshi:
    plugin_type = "player"
    id = "kboshi"
    name = "Kboshi"
    char_type = CharacterType.A

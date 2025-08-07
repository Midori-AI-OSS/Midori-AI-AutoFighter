from dataclasses import dataclass

from game.actors import CharacterType


@dataclass
class SamplePlayer:
    plugin_type = "player"
    id = "sample_player"
    name = "Sample Player"
    char_type = CharacterType.C

from dataclasses import dataclass

from autofighter.character import CharacterType
from plugins.players._base import PlayerBase

@dataclass
class Player(PlayerBase):
    id = "player"
    name = "Player"
    char_type = CharacterType.C
    damage_type: str = "Fire"
    prompt: str = "Player prompt placeholder"
    about: str = "Player description placeholder"

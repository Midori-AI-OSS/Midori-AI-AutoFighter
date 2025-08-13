from dataclasses import dataclass

from autofighter.character import CharacterType
from plugins.players._base import PlayerBase

@dataclass
class LadyEcho(PlayerBase):
    id = "lady_echo"
    name = "LadyEcho"
    char_type = CharacterType.B
    base_damage_type: str = "Lightning"


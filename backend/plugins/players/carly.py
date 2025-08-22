from dataclasses import dataclass

from autofighter.character import CharacterType
from plugins.players._base import PlayerBase

@dataclass
class Carly(PlayerBase):
    id = "carly"
    name = "Carly"
    char_type = CharacterType.B
    gacha_rarity = 5
    damage_type: str = "Light"


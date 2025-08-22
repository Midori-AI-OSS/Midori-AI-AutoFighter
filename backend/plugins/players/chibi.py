from dataclasses import dataclass
from dataclasses import field

from plugins.damage_types import get_damage_type
from autofighter.character import CharacterType
from plugins.players._base import PlayerBase

@dataclass
class Chibi(PlayerBase):
    id = "chibi"
    name = "Chibi"
    char_type = CharacterType.A
    gacha_rarity = 5
    damage_type: str = field(default_factory=lambda: get_damage_type("Chibi"))

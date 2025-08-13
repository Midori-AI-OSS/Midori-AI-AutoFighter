from dataclasses import dataclass
from dataclasses import field

from plugins.damage_types import get_damage_type
from autofighter.character import CharacterType
from plugins.players._base import PlayerBase

@dataclass
class LadyFireAndIce(PlayerBase):
    id = "lady_fire_and_ice"
    name = "LadyFireAndIce"
    char_type = CharacterType.B
    gacha_rarity = 6
    base_damage_type: str = field(default_factory=lambda: get_damage_type("LadyFireAndIce"))

from dataclasses import dataclass
from dataclasses import field

from plugins.damage_types import get_damage_type
from autofighter.character import CharacterType
from plugins.players._base import PlayerBase

@dataclass
class LadyOfFire(PlayerBase):
    id = "lady_of_fire"
    name = "LadyOfFire"
    char_type = CharacterType.B
    damage_type: str = field(default_factory=lambda: get_damage_type("LadyOfFire"))

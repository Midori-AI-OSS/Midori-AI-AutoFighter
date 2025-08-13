from dataclasses import dataclass
from dataclasses import field

from plugins.damage_types import get_damage_type
from autofighter.character import CharacterType
from plugins.players._base import PlayerBase

@dataclass
class LadyLight(PlayerBase):
    id = "lady_light"
    name = "LadyLight"
    char_type = CharacterType.B
    base_damage_type: str = field(default_factory=lambda: get_damage_type("LadyLight"))

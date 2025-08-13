from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class SturdyVest(CardBase):
    id: str = "sturdy_vest"
    name: str = "Sturdy Vest"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"max_hp": 0.03})

from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class SharpeningStone(CardBase):
    id: str = "sharpening_stone"
    name: str = "Sharpening Stone"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"crit_damage": 0.03})

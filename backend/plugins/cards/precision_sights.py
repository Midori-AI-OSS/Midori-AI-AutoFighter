from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class PrecisionSights(CardBase):
    id: str = "precision_sights"
    name: str = "Precision Sights"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"crit_damage": 0.04})

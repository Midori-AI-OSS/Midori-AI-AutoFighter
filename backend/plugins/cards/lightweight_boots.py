from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class LightweightBoots(CardBase):
    id: str = "lightweight_boots"
    name: str = "Lightweight Boots"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"dodge_odds": 0.03})

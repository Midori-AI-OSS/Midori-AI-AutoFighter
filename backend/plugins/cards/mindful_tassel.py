from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class MindfulTassel(CardBase):
    id: str = "mindful_tassel"
    name: str = "Mindful Tassel"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"effect_hit_rate": 0.03})

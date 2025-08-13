from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class MicroBlade(CardBase):
    id: str = "micro_blade"
    name: str = "Micro Blade"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"atk": 0.03})

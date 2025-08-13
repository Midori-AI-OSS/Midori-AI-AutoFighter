from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class PolishedShield(CardBase):
    id: str = "polished_shield"
    name: str = "Polished Shield"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"defense": 0.03})

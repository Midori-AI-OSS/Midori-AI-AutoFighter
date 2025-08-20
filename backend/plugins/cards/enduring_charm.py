from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class EnduringCharm(CardBase):
    id: str = "enduring_charm"
    name: str = "Enduring Charm"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"vitality": 0.03})

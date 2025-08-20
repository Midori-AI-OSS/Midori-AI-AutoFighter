from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class FortifiedPlating(CardBase):
    id: str = "fortified_plating"
    name: str = "Fortified Plating"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"defense": 0.04})

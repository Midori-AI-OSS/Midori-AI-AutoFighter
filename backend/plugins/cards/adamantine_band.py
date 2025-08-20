from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class AdamantineBand(CardBase):
    id: str = "adamantine_band"
    name: str = "Adamantine Band"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"max_hp": 0.04})

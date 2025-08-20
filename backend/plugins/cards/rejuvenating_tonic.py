from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class RejuvenatingTonic(CardBase):
    id: str = "rejuvenating_tonic"
    name: str = "Rejuvenating Tonic"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"regain": 0.04})

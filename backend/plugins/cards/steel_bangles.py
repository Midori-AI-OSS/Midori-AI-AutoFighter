from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class SteelBangles(CardBase):
    id: str = "steel_bangles"
    name: str = "Steel Bangles"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"mitigation": 0.03})

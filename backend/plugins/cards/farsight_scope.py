from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class FarsightScope(CardBase):
    id: str = "farsight_scope"
    name: str = "Farsight Scope"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"crit_rate": 0.03})

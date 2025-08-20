from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class ExpertManual(CardBase):
    id: str = "expert_manual"
    name: str = "Expert Manual"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"exp_multiplier": 0.03})

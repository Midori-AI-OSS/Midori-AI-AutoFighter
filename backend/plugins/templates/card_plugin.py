from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class SampleCard(CardBase):
    id: str = "sample_card"
    name: str = "Sample Card"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=dict)

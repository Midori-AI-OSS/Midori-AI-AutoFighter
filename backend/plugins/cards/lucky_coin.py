from dataclasses import dataclass
from dataclasses import field

from plugins.cards._base import CardBase


@dataclass
class LuckyCoin(CardBase):
    id: str = "lucky_coin"
    name: str = "Lucky Coin"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"crit_rate": 0.03})

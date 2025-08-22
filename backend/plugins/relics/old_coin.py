from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class OldCoin(RelicBase):
    """+3% gold earned; first shop purchase refunded 3% of cost."""

    id: str = "old_coin"
    name: str = "Old Coin"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=dict)
    about: str = "+3% gold earned; first shop purchase refunded 3% of cost."

    def apply(self, party) -> None:
        super().apply(party)

        first_purchase = {"done": False}

        def _gold(amount: int) -> None:
            party.gold += int(amount * 0.03)

        def _purchase(cost: int) -> None:
            if first_purchase["done"]:
                return
            party.gold += int(cost * 0.03)
            first_purchase["done"] = True

        BUS.subscribe("gold_earned", _gold)
        BUS.subscribe("shop_purchase", _purchase)

    def describe(self, stacks: int) -> str:
        rate = 3 * stacks
        return f"+{rate}% gold earned; first shop purchase refunded {rate}% of cost."

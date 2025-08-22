from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class PocketManual(RelicBase):
    """+3% damage; every 10th hit deals 3% extra Aftertaste damage."""

    id: str = "pocket_manual"
    name: str = "Pocket Manual"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"atk": 0.03})
    about: str = "+3% damage; every 10th hit deals +3% Aftertaste damage."

    def apply(self, party) -> None:
        super().apply(party)

        counts: dict[int, int] = {}

        def _hit(attacker, target, amount) -> None:
            pid = id(attacker)
            counts[pid] = counts.get(pid, 0) + 1
            if counts[pid] % 10 == 0:
                target.hp -= int(amount * 0.03)

        BUS.subscribe("hit_landed", _hit)

    def describe(self, stacks: int) -> str:
        dmg = 3 * stacks
        return f"+{dmg}% damage; every 10th hit deals +3% Aftertaste damage."

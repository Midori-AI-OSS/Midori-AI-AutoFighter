from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class FrostSigil(RelicBase):
    """Hits apply chill dealing 5% ATK as Aftertaste per stack."""

    id: str = "frost_sigil"
    name: str = "Frost Sigil"
    stars: int = 2
    effects: dict[str, float] = field(default_factory=dict)
    about: str = "Hits apply chill dealing 5% ATK as Aftertaste per stack."

    def apply(self, party) -> None:
        super().apply(party)

        def _hit(attacker, target, amount) -> None:
            target.hp -= int(attacker.atk * 0.05)

        BUS.subscribe("hit_landed", _hit)

    def describe(self, stacks: int) -> str:
        pct = 5 * stacks
        return f"Hits apply chill dealing {pct}% ATK as Aftertaste."

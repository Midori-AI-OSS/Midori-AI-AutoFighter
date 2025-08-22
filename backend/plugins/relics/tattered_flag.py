from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class TatteredFlag(RelicBase):
    """+3% party Max HP; ally deaths grant survivors +3% ATK."""

    id: str = "tattered_flag"
    name: str = "Tattered Flag"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"max_hp": 0.03})
    about: str = "+3% party Max HP; ally deaths grant survivors +3% ATK."

    def apply(self, party) -> None:
        super().apply(party)

        def _fallen(target, attacker, amount) -> None:
            if target not in party.members or target.hp > 0:
                return
            for member in party.members:
                if member is not target and member.hp > 0:
                    member.atk = int(member.atk * 1.03)

        BUS.subscribe("damage_taken", _fallen)

    def describe(self, stacks: int) -> str:
        hp = 3 * stacks
        return f"+{hp}% party Max HP; ally deaths grant survivors +3% ATK."

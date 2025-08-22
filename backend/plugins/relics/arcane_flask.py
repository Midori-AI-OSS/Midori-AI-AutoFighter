from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class ArcaneFlask(RelicBase):
    """After an Ultimate, grant a shield equal to 20% Max HP per stack."""

    id: str = "arcane_flask"
    name: str = "Arcane Flask"
    stars: int = 2
    effects: dict[str, float] = field(default_factory=dict)
    about: str = "After an Ultimate, grant a shield equal to 20% Max HP." 

    def apply(self, party) -> None:
        super().apply(party)

        def _ultimate(user) -> None:
            user.hp = min(user.max_hp, user.hp + int(user.max_hp * 0.2))

        BUS.subscribe("ultimate_used", _ultimate)

    def describe(self, stacks: int) -> str:
        pct = 20 * stacks
        return f"After an Ultimate, grant a shield equal to {pct}% Max HP."

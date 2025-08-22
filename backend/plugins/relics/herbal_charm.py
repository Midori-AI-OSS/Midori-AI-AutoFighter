from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class HerbalCharm(RelicBase):
    """Heals all allies for 0.5% Max HP at the start of each turn."""

    id: str = "herbal_charm"
    name: str = "Herbal Charm"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {})
    about: str = "Heals all allies for 0.5% Max HP at the start of each turn per stack."

    def apply(self, party) -> None:
        def _heal(*_) -> None:
            for member in party.members:
                heal = int(member.max_hp * 0.005)
                member.hp = min(member.hp + heal, member.max_hp)

        BUS.subscribe("turn_start", _heal)

    def describe(self, stacks: int) -> str:
        pct = 0.5 * stacks
        return f"Heals all allies for {pct}% Max HP at the start of each turn."

from dataclasses import field
from dataclasses import dataclass

from autofighter.stats import BUS
from plugins.relics._base import RelicBase


@dataclass
class ShinyPebble(RelicBase):
    """Raises DEF and gives a mitigation burst on the first hit."""

    id: str = "shiny_pebble"
    name: str = "Shiny Pebble"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"defense": 0.03})
    about: str = (
        "Boosts DEF and grants extra mitigation the first time an ally is hit."
    )

    def apply(self, party) -> None:
        super().apply(party)

        triggered: set[int] = set()
        to_remove: dict[int, object] = {}
        stacks = party.relics.count(self.id)
        mit_mult = 1 + 0.03 * stacks

        def _first_hit(target, attacker, amount) -> None:
            if target not in party.members or id(target) in triggered:
                return
            triggered.add(id(target))
            to_remove[id(target)] = target
            target.mitigation *= mit_mult

        def _reset(*_) -> None:
            for key, member in list(to_remove.items()):
                member.mitigation /= mit_mult
                to_remove.pop(key, None)

        BUS.subscribe("damage_taken", _first_hit)
        BUS.subscribe("turn_start", _reset)

    def describe(self, stacks: int) -> str:
        defense = 3 * stacks
        mit = 3 * stacks
        return (
            f"+{defense}% DEF. The first time each ally is hit, they gain +{mit}% mitigation for one turn."
        )

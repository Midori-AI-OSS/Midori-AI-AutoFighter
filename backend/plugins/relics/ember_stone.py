from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class EmberStone(RelicBase):
    """Burn attacker for 50% ATK when a low-HP ally is struck."""

    id: str = "ember_stone"
    name: str = "Ember Stone"
    stars: int = 2
    effects: dict[str, float] = field(default_factory=dict)
    about: str = "Below 25% HP, burn the attacker for 50% ATK per stack."

    def apply(self, party) -> None:
        def _burn(target, attacker, amount) -> None:
            if attacker is None or target not in party.members:
                return
            if target.hp <= target.max_hp * 0.25:
                attacker.hp = max(attacker.hp - int(target.atk * 0.5), 0)
        BUS.subscribe("damage_taken", _burn)

    def describe(self, stacks: int) -> str:
        pct = 50 * stacks
        return f"Below 25% HP, burn the attacker for {pct}% ATK."

from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class VengefulPendant(RelicBase):
    """Reflects 15% of damage taken back to the attacker."""

    id: str = "vengeful_pendant"
    name: str = "Vengeful Pendant"
    stars: int = 2
    effects: dict[str, float] = field(default_factory=dict)
    about: str = "Reflects 15% of damage taken back to the attacker."

    def apply(self, party) -> None:
        def _reflect(target, attacker, amount) -> None:
            if attacker is None or target not in party.members:
                return
            attacker.hp = max(attacker.hp - int(amount * 0.15), 0)
        BUS.subscribe("damage_taken", _reflect)

    def describe(self, stacks: int) -> str:
        pct = 15 * stacks
        return f"Reflects {pct}% of damage taken back to the attacker."

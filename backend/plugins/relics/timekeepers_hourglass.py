from dataclasses import dataclass
from dataclasses import field
import random

from plugins.relics._base import RelicBase
from autofighter.stats import BUS


@dataclass
class TimekeepersHourglass(RelicBase):
    """Each turn, 10% +1% per stack chance for allies to gain an extra turn."""

    id: str = "timekeepers_hourglass"
    name: str = "Timekeeper's Hourglass"
    stars: int = 4
    effects: dict[str, float] = field(default_factory=dict)
    about: str = "Each turn, 10% +1% per stack chance for allies to gain an extra turn."

    def apply(self, party) -> None:
        if getattr(party, "_t_hourglass_applied", False):
            return
        party._t_hourglass_applied = True
        super().apply(party)

        stacks = party.relics.count(self.id)
        chance = 0.10 + 0.01 * (stacks - 1)

        def _turn_start() -> None:
            if random.random() < chance:
                for member in party.members:
                    BUS.emit("extra_turn", member)

        BUS.subscribe("turn_start", _turn_start)

    def describe(self, stacks: int) -> str:
        pct = 10 + 1 * (stacks - 1)
        return f"Each turn, {pct}% chance for allies to gain an extra turn."

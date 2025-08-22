from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS
from plugins.players._base import PlayerBase


@dataclass
class WoodenIdol(RelicBase):
    """+3% Effect Res; resisting a debuff grants +1% Effect Res next turn."""

    id: str = "wooden_idol"
    name: str = "Wooden Idol"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"effect_resistance": 0.03})
    about: str = "+3% Effect Res; resisting a debuff grants +1% Effect Res next turn."

    def apply(self, party) -> None:
        super().apply(party)

        pending: dict[int, float] = {}
        active: dict[int, tuple[PlayerBase, float]] = {}

        def _resisted(member) -> None:
            pid = id(member)
            pending[pid] = pending.get(pid, 0) + 0.01

        def _turn_start() -> None:
            for pid, bonus in list(pending.items()):
                member = next((m for m in party.members if id(m) == pid), None)
                if member is None:
                    continue
                member.effect_resistance += bonus
                active[pid] = (member, bonus)
            pending.clear()

        def _turn_end() -> None:
            for pid, (member, bonus) in list(active.items()):
                member.effect_resistance -= bonus
            active.clear()

        BUS.subscribe("debuff_resisted", _resisted)
        BUS.subscribe("turn_start", lambda: _turn_start())
        BUS.subscribe("turn_end", lambda: _turn_end())

    def describe(self, stacks: int) -> str:
        res = 3 * stacks
        return (
            f"+{res}% Effect Res; resisting a debuff grants +1% Effect Res next turn."
        )

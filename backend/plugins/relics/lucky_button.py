from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS
from plugins.players._base import PlayerBase


@dataclass
class LuckyButton(RelicBase):
    """+3% Crit Rate; missed crits add +3% Crit Rate next turn."""

    id: str = "lucky_button"
    name: str = "Lucky Button"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {"crit_rate": 0.03})
    about: str = "+3% Crit Rate; missed crits add +3% Crit Rate next turn."

    def apply(self, party) -> None:
        super().apply(party)

        pending: dict[int, float] = {}
        active: dict[int, tuple[PlayerBase, float]] = {}

        def _crit_missed(attacker, target) -> None:
            pid = id(attacker)
            pending[pid] = pending.get(pid, 0) + 0.03

        def _turn_start() -> None:
            for pid, bonus in list(pending.items()):
                member = next((m for m in party.members if id(m) == pid), None)
                if member is None:
                    continue
                member.crit_rate += bonus
                active[pid] = (member, bonus)
            pending.clear()

        def _turn_end() -> None:
            for pid, (member, bonus) in list(active.items()):
                member.crit_rate -= bonus
            active.clear()

        BUS.subscribe("crit_missed", _crit_missed)
        BUS.subscribe("turn_start", lambda: _turn_start())
        BUS.subscribe("turn_end", lambda: _turn_end())

    def describe(self, stacks: int) -> str:
        rate = 3 * stacks
        return f"+{rate}% Crit Rate; missed crits add +{rate}% Crit Rate next turn."

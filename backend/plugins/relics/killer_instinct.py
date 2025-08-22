from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase
from autofighter.stats import BUS
from plugins.players._base import PlayerBase


@dataclass
class KillerInstinct(RelicBase):
    """Ultimates grant +75% ATK for the turn; kills grant another turn."""

    id: str = "killer_instinct"
    name: str = "Killer Instinct"
    stars: int = 2
    effects: dict[str, float] = field(default_factory=dict)
    about: str = "Ultimates grant +75% ATK for the turn; kills grant another turn."

    def apply(self, party) -> None:
        super().apply(party)

        buffs: dict[int, tuple[PlayerBase, int]] = {}

        def _ultimate(user) -> None:
            bonus = int(user.atk * 0.75)
            user.atk += bonus
            buffs[id(user)] = (user, bonus)

        def _damage(target, attacker, amount) -> None:
            if target.hp <= 0 and id(attacker) in buffs:
                BUS.emit("extra_turn", attacker)

        def _turn_end() -> None:
            for _, (member, bonus) in list(buffs.items()):
                member.atk -= bonus
            buffs.clear()

        BUS.subscribe("ultimate_used", _ultimate)
        BUS.subscribe("damage_taken", _damage)
        BUS.subscribe("turn_end", lambda: _turn_end())

    def describe(self, stacks: int) -> str:
        pct = 75 * stacks
        return f"Ultimates grant +{pct}% ATK for the turn; kills grant another turn."

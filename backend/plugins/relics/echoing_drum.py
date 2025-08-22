from dataclasses import dataclass
from dataclasses import field

from autofighter.stats import BUS
from plugins.relics._base import RelicBase


@dataclass
class EchoingDrum(RelicBase):
    """First attack each battle repeats at 25% power per stack."""

    id: str = "echoing_drum"
    name: str = "Echoing Drum"
    stars: int = 3
    effects: dict[str, float] = field(default_factory=lambda: {})
    about: str = "First attack each battle repeats at 25% power per stack."

    def apply(self, party) -> None:
        super().apply(party)

        used: set[int] = set()

        def _battle_start() -> None:
            used.clear()

        def _attack(attacker, target, amount) -> None:
            pid = id(attacker)
            if pid in used:
                return
            used.add(pid)
            target.hp -= int(amount * 0.25)

        BUS.subscribe("battle_start", lambda: _battle_start())
        BUS.subscribe("attack_used", _attack)

    def describe(self, stacks: int) -> str:
        pct = 25 * stacks
        return f"First attack each battle repeats at {pct}% power."

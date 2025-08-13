from __future__ import annotations

from dataclasses import dataclass

from .party import Party


@dataclass(frozen=True)
class Relic:
    id: str
    name: str
    effects: dict[str, float]

    def apply(self, party: Party) -> None:
        for member in party.members:
            for attr, pct in self.effects.items():
                value = getattr(member, attr, None)
                if value is None:
                    continue
                new_value = type(value)(value * (1 + pct))
                setattr(member, attr, new_value)


RELIC_LIBRARY: dict[str, Relic] = {}


def apply_relics(party: Party) -> None:
    for rid in party.relics:
        relic = RELIC_LIBRARY.get(rid)
        if relic:
            relic.apply(party)

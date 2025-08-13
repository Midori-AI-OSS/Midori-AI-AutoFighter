from dataclasses import dataclass
from dataclasses import field

from autofighter.party import Party


@dataclass
class CardBase:
    plugin_type = "card"

    id: str = ""
    name: str = ""
    stars: int = 1
    effects: dict[str, float] = field(default_factory=dict)

    def apply(self, party: Party) -> None:
        for member in party.members:
            for attr, pct in self.effects.items():
                if attr == "max_hp":
                    member.max_hp = type(member.max_hp)(member.max_hp * (1 + pct))
                    member.hp = type(member.hp)(member.hp * (1 + pct))
                else:
                    value = getattr(member, attr, None)
                    if value is None:
                        continue
                    new_value = type(value)(value * (1 + pct))
                    setattr(member, attr, new_value)

from dataclasses import dataclass
from dataclasses import field

from autofighter.stats import BUS
from plugins.relics._base import RelicBase


@dataclass
class NullLantern(RelicBase):
    """Removes shops/rests and converts fights into pulls."""

    id: str = "null_lantern"
    name: str = "Null Lantern"
    stars: int = 4
    effects: dict[str, float] = field(default_factory=lambda: {})

    def apply(self, party) -> None:
        """Disable shops/rests, buff foes, and award pull tokens."""
        super().apply(party)

        party.no_shops = True
        party.no_rests = True
        stacks = party.relics.count(self.id)
        state = {"cleared": 0}

        if not hasattr(party, "pull_tokens"):
            party.pull_tokens = 0

        def _battle_start(entity) -> None:
            from plugins.foes._base import FoeBase

            if isinstance(entity, FoeBase):
                mult = 1 + 1.5 * state["cleared"]
                entity.atk = int(entity.atk * mult)
                entity.defense = int(entity.defense * mult)
                entity.max_hp = int(entity.max_hp * mult)
                entity.hp = entity.max_hp

        def _battle_end(entity) -> None:
            from plugins.foes._base import FoeBase

            if isinstance(entity, FoeBase):
                state["cleared"] += 1
                party.pull_tokens += 1 + (stacks - 1)

        BUS.subscribe("battle_start", _battle_start)
        BUS.subscribe("battle_end", _battle_end)

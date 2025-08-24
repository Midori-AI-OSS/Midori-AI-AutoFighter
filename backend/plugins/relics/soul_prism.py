from dataclasses import dataclass
from dataclasses import field

from autofighter.stats import BUS
from plugins.relics._base import RelicBase


@dataclass
class SoulPrism(RelicBase):
    """Revives fallen allies at 1% HP with heavy Max HP penalty and small buffs."""

    id: str = "soul_prism"
    name: str = "Soul Prism"
    stars: int = 5
    effects: dict[str, float] = field(default_factory=lambda: {"defense": 0.05, "mitigation": 0.05})
    about: str = "Revives fallen allies at 1% HP with heavy Max HP penalty and small buffs."

    def apply(self, party) -> None:
        """Revive fallen allies after battles with reduced Max HP."""
        super().apply(party)

        stacks = party.relics.count(self.id)
        penalty = 0.75 - 0.05 * (stacks - 1)
        multiplier = 1 - penalty
        buff = 0.05 + 0.02 * (stacks - 1)

        def _battle_end(entity) -> None:
            from plugins.foes._base import FoeBase

            if not isinstance(entity, FoeBase):
                return
            for member in party.members:
                if member.hp > 0:
                    continue
                base = getattr(member, "_soul_prism_hp", member.max_hp)
                member._soul_prism_hp = base
                member.max_hp = int(base * multiplier)
                member.hp = max(1, int(member.max_hp * 0.01))
                new_def = int(member.defense * (1 + buff))
                member.adjust_stat_on_gain("defense", new_def - member.defense)
                new_mit = member.mitigation * (1 + buff)
                member.adjust_stat_on_gain("mitigation", new_mit - member.mitigation)

        BUS.subscribe("battle_end", _battle_end)

    def describe(self, stacks: int) -> str:
        penalty = 75 - 5 * (stacks - 1)
        buff = 5 + 2 * (stacks - 1)
        return (
            "Revives fallen allies at 1% HP after battles. "
            f"Reduces Max HP by {penalty}% and grants +{buff}% DEF and mitigation."
        )

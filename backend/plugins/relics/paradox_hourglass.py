"""Paradox Hourglass relic effects."""

import random
from dataclasses import dataclass
from dataclasses import field

from autofighter.stats import BUS
from plugins.relics._base import RelicBase


@dataclass
class ParadoxHourglass(RelicBase):
    """Can sacrifice allies at battle start to supercharge survivors and debuff foes."""

    id: str = "paradox_hourglass"
    name: str = "Paradox Hourglass"
    stars: int = 5
    effects: dict[str, float] = field(default_factory=lambda: {"atk": 2.0, "defense": 2.0})
    about: str = (
        "At battle start may sacrifice allies to supercharge survivors and shred foe defense."
    )

    def apply(self, party) -> None:
        """On battle start possibly sacrifices allies for massive buffs."""
        super().apply(party)

        stacks = party.relics.count(self.id)
        state: dict[str, dict] = {"buffs": {}, "foe": {}}

        def _battle_start(entity) -> None:
            from plugins.foes._base import FoeBase

            if isinstance(entity, FoeBase):
                base_def = entity.defense
                div = 4 + (stacks - 1)
                entity.defense = max(100, int(base_def / div))
                state["foe"][id(entity)] = base_def
                return

            if state.get("done"):
                return
            state["done"] = True

            alive = [m for m in party.members if m.hp > 0]
            if len(alive) <= 1:
                return
            chance = 0.6 * (len(alive) - 1) / len(alive)
            if random.random() >= chance:
                return
            kill_count = min(stacks, 4, len(alive) - 1)
            to_kill = random.sample(alive, kill_count)
            for m in to_kill:
                m.hp = 0
            survivors = [m for m in party.members if m.hp > 0]
            mult = 3 + (stacks - 1)
            for m in survivors:
                state["buffs"][id(m)] = {
                    "atk": m.atk,
                    "defense": m.defense,
                    "max_hp": m.max_hp,
                    "crit_rate": m.crit_rate,
                    "crit_damage": m.crit_damage,
                    "effect_hit_rate": m.effect_hit_rate,
                    "effect_resistance": m.effect_resistance,
                    "vitality": m.vitality,
                    "mitigation": m.mitigation,
                }
                m.atk = int(m.atk * mult)
                m.defense = int(m.defense * mult)
                m.max_hp = int(m.max_hp * mult)
                m.hp = m.max_hp
                m.crit_rate *= mult
                m.crit_damage *= mult
                m.effect_hit_rate *= mult
                m.effect_resistance *= mult
                m.vitality *= mult
                m.mitigation *= mult

        def _battle_end(entity) -> None:
            from plugins.foes._base import FoeBase

            if isinstance(entity, FoeBase):
                base = state["foe"].pop(id(entity), None)
                if base is not None:
                    entity.defense = base
                return

            if state.get("buffs"):
                for member in party.members:
                    base = state["buffs"].get(id(member))
                    if base:
                        member.atk = base["atk"]
                        member.defense = base["defense"]
                        member.max_hp = base["max_hp"]
                        member.hp = min(member.hp, member.max_hp)
                        member.crit_rate = base["crit_rate"]
                        member.crit_damage = base["crit_damage"]
                        member.effect_hit_rate = base["effect_hit_rate"]
                        member.effect_resistance = base["effect_resistance"]
                        member.vitality = base["vitality"]
                        member.mitigation = base["mitigation"]
                state["buffs"].clear()
                state.pop("done", None)

        BUS.subscribe("battle_start", _battle_start)
        BUS.subscribe("battle_end", _battle_end)

    def describe(self, stacks: int) -> str:
        div = 4 + (stacks - 1)
        mult = 3 + (stacks - 1)
        kill = min(stacks, 4)
        return (
            f"60% chance to sacrifice up to {kill} random allies (max 4). "
            f"Survivors gain {mult}x stats and foes' DEF is divided by {div}."
        )

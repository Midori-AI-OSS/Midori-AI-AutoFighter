"""Omega Core relic effects."""

from dataclasses import dataclass
from dataclasses import field

from autofighter.stats import BUS
from plugins.relics._base import RelicBase


@dataclass
class OmegaCore(RelicBase):
    """Massive stat boost for 10 turns, then escalating HP drain."""

    id: str = "omega_core"
    name: str = "Omega Core"
    stars: int = 5
    effects: dict[str, float] = field(default_factory=lambda: {"atk": 5.0, "defense": 5.0})

    def apply(self, party) -> None:
        """Burst of power followed by increasing HP drain."""
        super().apply(party)

        stacks = party.relics.count(self.id)
        delay = 10 + 2 * (stacks - 1)
        mult = 6.0
        state = {"bases": {}, "turn": 0}

        def _battle_start(entity) -> None:
            from plugins.foes._base import FoeBase

            if isinstance(entity, FoeBase) or state["bases"]:
                return
            for member in party.members:
                state["bases"][id(member)] = {
                    "atk": member.atk,
                    "defense": member.defense,
                    "max_hp": member.max_hp,
                    "crit_rate": member.crit_rate,
                    "crit_damage": member.crit_damage,
                    "effect_hit_rate": member.effect_hit_rate,
                    "effect_resistance": member.effect_resistance,
                    "vitality": member.vitality,
                    "mitigation": member.mitigation,
                }
                member.atk = int(member.atk * mult)
                member.defense = int(member.defense * mult)
                member.max_hp = int(member.max_hp * mult)
                member.hp = member.max_hp
                member.crit_rate *= mult
                member.crit_damage *= mult
                member.effect_hit_rate *= mult
                member.effect_resistance *= mult
                member.vitality *= mult
                member.mitigation *= mult
            state["turn"] = 0

        def _turn_start() -> None:
            if not state["bases"]:
                return
            state["turn"] += 1
            if state["turn"] <= delay:
                return
            drain = (state["turn"] - delay) * 0.01
            for member in party.members:
                dmg = int(member.max_hp * drain)
                member.hp = max(member.hp - dmg, 0)

        def _battle_end(entity) -> None:
            from plugins.foes._base import FoeBase

            if not isinstance(entity, FoeBase):
                return
            for member in party.members:
                base = state["bases"].get(id(member))
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
            state["bases"].clear()

        BUS.subscribe("battle_start", _battle_start)
        BUS.subscribe("turn_start", _turn_start)
        BUS.subscribe("battle_end", _battle_end)

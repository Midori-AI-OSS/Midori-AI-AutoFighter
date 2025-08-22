import random
import asyncio

from dataclasses import field
from dataclasses import dataclass

from autofighter.stats import BUS
from plugins.relics._base import RelicBase
from plugins.effects.aftertaste import Aftertaste


@dataclass
class RustyBuckle(RelicBase):
    """Bleeds lowest-HP ally and triggers Aftertaste as HP drops."""

    id: str = "rusty_buckle"
    name: str = "Rusty Buckle"
    stars: int = 1
    effects: dict[str, float] = field(default_factory=lambda: {})
    about: str = (
        "Bleeds the weakest ally and unleashes growing Aftertaste blasts as they suffer."
    )

    def apply(self, party) -> None:
        """Bleed weakest ally and ping foes as their HP drops."""
        super().apply(party)

        stacks = party.relics.count(self.id)
        state: dict[str, object] = {"foes": [], "ally": None, "triggers": 0}

        def _battle_start(entity) -> None:
            from plugins.foes._base import FoeBase

            if isinstance(entity, FoeBase):
                state["foes"].append(entity)
                return

            if state["ally"] is None and party.members:
                ally = min(party.members, key=lambda m: m.max_hp)
                bleed = int(ally.max_hp * 0.01 * stacks)
                ally.hp = max(ally.hp - bleed, 1)
                state["ally"] = ally
                state["triggers"] = 0

        def _damage(target, attacker, amount) -> None:
            ally = state.get("ally")
            if target is not ally:
                return
            max_hp = ally.max_hp
            triggers = state["triggers"]
            lost_frac = 1 - (ally.hp / max_hp)
            while lost_frac >= 0.1 * (triggers + 1):
                triggers += 1
                state["triggers"] = triggers
                total_lost = max_hp * 0.1 * triggers
                dmg = int(total_lost * 0.005)
                hits = 5 + 3 * (stacks - 1)
                for _ in range(hits):
                    if state["foes"]:
                        foe = random.choice(state["foes"])
                        asyncio.create_task(Aftertaste(base_pot=dmg).apply(ally, foe))

        BUS.subscribe("battle_start", _battle_start)
        BUS.subscribe("damage_taken", _damage)

    def describe(self, stacks: int) -> str:
        bleed = 1 * stacks
        hits = 5 + 3 * (stacks - 1)
        return (
            f"Lowest-HP ally bleeds for {bleed}% Max HP at start. "
            f"Each 10% HP lost triggers {hits} Aftertaste hits at random foes."
        )

from __future__ import annotations

import random

from dataclasses import dataclass
from typing import List
from typing import Optional

from rich.console import Console

from autofighter.stats import Stats


@dataclass
class DamageOverTime:
    """Base class for damage over time effects."""

    name: str
    damage: int
    turns: int
    id: str
    source: Optional[Stats] = None

    async def tick(self, target: Stats, *_: object) -> bool:
        attacker = self.source or target
        dmg = target.damage_type.on_dot_damage_taken(
            self.damage,
            attacker,
            target,
        )
        dmg = target.damage_type.on_party_dot_damage_taken(
            dmg,
            attacker,
            target,
        )
        source_type = getattr(attacker, "damage_type", None)
        if source_type is not target.damage_type:
            dmg = source_type.on_party_dot_damage_taken(dmg, attacker, target)
        await target.apply_damage(int(dmg), attacker=attacker)
        self.turns -= 1
        return self.turns > 0


@dataclass
class HealingOverTime:
    """Base class for healing over time effects."""

    name: str
    healing: int
    turns: int
    id: str
    source: Optional[Stats] = None

    async def tick(self, target: Stats, *_: object) -> bool:
        healer = self.source or target
        heal = target.damage_type.on_hot_heal_received(self.healing, healer, target)
        heal = target.damage_type.on_party_hot_heal_received(heal, healer, target)
        await target.apply_healing(int(heal), healer=healer)
        self.turns -= 1
        return self.turns > 0


class EffectManager:
    """Manage DoT and HoT effects on a Stats object."""

    def __init__(self, stats: Stats) -> None:
        self.stats = stats
        self.dots: List[DamageOverTime] = []
        self.hots: List[HealingOverTime] = []
        self._console = Console()

    def add_dot(self, effect: DamageOverTime, max_stacks: Optional[int] = None) -> None:
        """Attach a DoT instance to the tracked stats.

        DoTs with the same ``id`` stack independently, allowing multiple
        copies to tick each turn.  When ``max_stacks`` is provided, extra
        applications beyond that limit are ignored rather than refreshed.
        """

        if max_stacks is not None:
            current = len([d for d in self.dots if d.id == effect.id])
            if current >= max_stacks:
                return
        self.dots.append(effect)
        self.stats.dots.append(effect.id)

    def add_hot(self, effect: HealingOverTime) -> None:
        """Attach a HoT instance to the tracked stats.

        Healing effects simply accumulate; each copy heals separately every
        tick with no inherent stack cap.
        """

        self.hots.append(effect)
        self.stats.hots.append(effect.id)

    def maybe_inflict_dot(self, attacker: Stats, damage: int) -> None:
        dot = attacker.damage_type.create_dot(damage, attacker)
        if dot is None:
            return
        rate = max(attacker.effect_hit_rate - self.stats.effect_resistance, 0.0)
        chance = max(min(rate * random.uniform(0.9, 1.1), 1.0), 0.01)
        if random.random() < chance:
            self.add_dot(dot)

    async def tick(self, others: Optional[EffectManager] = None) -> None:
        for collection, names in (
            (self.hots, self.stats.hots),
            (self.dots, self.stats.dots),
        ):
            expired: List[object] = []
            for eff in collection:
                color = "green" if isinstance(eff, HealingOverTime) else "light_red"
                self._console.log(
                    f"[{color}]{self.stats.id} {eff.name} tick[/]"
                )
                if not await eff.tick(self.stats):
                    expired.append(eff)
            for eff in expired:
                collection.remove(eff)
                if eff.id in names:
                    names.remove(eff.id)
        if self.stats.hp <= 0 and others is not None:
            for eff in list(self.dots):
                on_death = getattr(eff, "on_death", None)
                if callable(on_death):
                    on_death(others)

    async def on_action(self) -> bool:
        """Run any per-action hooks on attached effects.

        Returns ``False`` if any effect cancels the action.
        """

        for eff in list(self.dots) + list(self.hots):
            handler = getattr(eff, "on_action", None)
            if callable(handler):
                self._console.log(f"{self.stats.id} {eff.name} action")
                result = handler(self.stats)
                if hasattr(result, "__await"):
                    result = await result
                if result is False:
                    return False
        return True

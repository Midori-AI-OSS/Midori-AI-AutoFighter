from __future__ import annotations

from typing import List
from typing import Iterable
from dataclasses import dataclass

from autofighter.stats import Stats


@dataclass
class DamageOverTime:
    """Simple damage-over-time effect."""

    name: str
    damage: int
    turns: int
    id: str

    plugin_type: str = "dot"

    def tick(self, target: Stats, *_) -> bool:
        target.apply_damage(self.damage)
        self.turns -= 1
        return self.turns > 0


@dataclass
class HealingOverTime:
    """Simple healing-over-time effect."""

    name: str
    healing: int
    turns: int
    id: str

    plugin_type: str = "hot"

    def tick(self, target: Stats, *_) -> bool:
        target.apply_healing(self.healing)
        self.turns -= 1
        return self.turns > 0


class EffectManager:
    """Tracks active DOT and HOT effects on a target."""

    def __init__(self, stats: Stats) -> None:
        self.stats = stats
        self.dots: List[DamageOverTime] = []
        self.hots: List[HealingOverTime] = []

    def add_dot(self, effect: DamageOverTime, *, max_stacks: int | None = None) -> None:
        max_stacks = max_stacks or getattr(effect, "max_stacks", None)
        if max_stacks is not None:
            current = [d for d in self.dots if d.id == effect.id]
            if len(current) >= max_stacks:
                return
        self.dots.append(effect)

    def add_hot(self, effect: HealingOverTime) -> None:
        self.hots.append(effect)

    def tick(self, others: Iterable[EffectManager] | None = None) -> None:
        remaining: List[DamageOverTime] = []
        for dot in self.dots:
            alive = dot.tick(self.stats)
            if self.stats.hp == 0 and others and hasattr(dot, "on_death"):
                for other in others:
                    dot.on_death(other)
            if alive:
                remaining.append(dot)
        self.dots = remaining
        self.hots = [h for h in self.hots if h.tick(self.stats)]

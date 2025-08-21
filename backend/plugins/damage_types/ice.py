from dataclasses import dataclass

from autofighter.effects import DamageOverTime
from plugins.dots.frozen_wound import FrozenWound
from plugins.damage_types._base import DamageTypeBase


@dataclass
class Ice(DamageTypeBase):
    id = "Ice"
    weakness = "Fire"
    color = (0, 255, 255)

    def create_dot(self, damage: float, source) -> DamageOverTime | None:
        dot = FrozenWound(int(damage * 0.25), 3)
        dot.source = source
        return dot

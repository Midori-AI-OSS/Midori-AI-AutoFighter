from dataclasses import dataclass

from autofighter.stats import Stats
from autofighter.effects import DamageOverTime
from plugins.dots.blazing_torment import BlazingTorment
from plugins.damage_types._base import DamageTypeBase


@dataclass
class Fire(DamageTypeBase):
    id = "Fire"
    weakness = "Ice"
    color = (255, 0, 0)

    def create_dot(self, damage: float, source) -> DamageOverTime | None:
        dot = BlazingTorment(int(damage * 0.5), 3)
        dot.source = source
        return dot

    def on_damage(self, damage: float, attacker: Stats, target: Stats) -> float:
        if attacker.max_hp <= 0:
            return damage
        missing_ratio = 1 - (attacker.hp / attacker.max_hp)
        return damage * (1 + missing_ratio)

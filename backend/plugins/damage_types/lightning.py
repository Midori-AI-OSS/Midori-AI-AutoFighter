import asyncio
from dataclasses import dataclass

from autofighter.effects import DamageOverTime
from plugins.dots.charged_decay import ChargedDecay
from plugins.damage_types._base import DamageTypeBase


@dataclass
class Lightning(DamageTypeBase):
    id = "Lightning"
    weakness = "Wind"
    color = (255, 255, 0)

    def create_dot(self, damage: float, source) -> DamageOverTime | None:
        dot = ChargedDecay(int(damage * 0.25), 3)
        dot.source = source
        return dot

    def on_hit(self, attacker, target) -> None:
        mgr = getattr(target, "effect_manager", None)
        if mgr is None:
            return
        for effect in list(mgr.dots):
            dmg = int(effect.damage * 0.25)
            if dmg > 0:
                asyncio.create_task(target.apply_damage(dmg, attacker=attacker))

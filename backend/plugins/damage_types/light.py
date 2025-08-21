from dataclasses import dataclass

from autofighter.effects import DamageOverTime
from plugins.damage_types._base import DamageTypeBase
from plugins.hots.radiant_regeneration import RadiantRegeneration


@dataclass
class Light(DamageTypeBase):
    id = "Light"
    weakness = "Dark"
    color = (255, 255, 255)

    def create_dot(self, damage: float, source) -> DamageOverTime | None:
        return DamageOverTime("Celestial Atrophy", int(damage * 0.3), 3, "light_dot", source)

    async def on_action(self, actor, allies, enemies):
        for ally in allies:
            ally.effect_manager.add_hot(RadiantRegeneration())
        for ally in allies:
            if ally.hp > 0 and ally.hp / ally.max_hp < 0.25:
                await ally.apply_healing(actor.atk, healer=actor)
                return False
        return True

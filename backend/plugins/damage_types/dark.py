from dataclasses import dataclass

from autofighter.effects import DamageOverTime
from autofighter.stats import BUS
from plugins.dots.shadow_siphon import ShadowSiphon
from plugins.damage_types._base import DamageTypeBase


@dataclass
class Dark(DamageTypeBase):
    id = "Dark"
    weakness = "Light"
    color = (145, 0, 145)

    _cleanup_registered: bool = False

    async def on_action(self, actor, allies, enemies) -> bool:
        for member in allies:
            mgr = getattr(member, "effect_manager", None)
            if mgr is not None:
                dmg = int(member.max_hp * 0.05)
                mgr.add_dot(ShadowSiphon(dmg))

        if not self._cleanup_registered:
            def _clear(_):
                for member in allies:
                    member.dots = [d for d in member.dots if d != ShadowSiphon.id]
                    mgr = getattr(member, "effect_manager", None)
                    if mgr is not None:
                        mgr.dots = [d for d in mgr.dots if getattr(d, "id", "") != ShadowSiphon.id]
                self._cleanup_registered = False

            BUS.subscribe("battle_end", _clear)
            self._cleanup_registered = True

        return True

    def on_party_dot_damage_taken(self, damage, attacker, target) -> float:
        if getattr(attacker, "base_damage_type", None) is self and ShadowSiphon.id in target.dots:
            percent = damage / target.max_hp
            attacker.atk *= 1 + percent
            attacker.defense *= 1 + percent
        return damage

    def create_dot(self, damage: float, source) -> DamageOverTime | None:
        return DamageOverTime(
            "Abyssal Corruption",
            int(damage * 0.4),
            3,
            "dark_dot",
            source,
        )

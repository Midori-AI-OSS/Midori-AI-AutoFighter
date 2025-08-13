from typing import Callable

from dataclasses import dataclass
from dataclasses import field

from plugins.damage_types._base import DamageTypeBase
from plugins.damage_types.generic import Generic

@dataclass
class Stats:
    hp: int = 1000
    max_hp: int = 1000
    exp: int = 0
    level: int = 1
    exp_multiplier: float = 1.0
    actions_per_turn: int = 1

    atk: int = 200
    crit_rate: float = 0.05
    crit_damage: float = 2.0
    effect_hit_rate: float = 1.0
    base_damage_type: DamageTypeBase = field(default_factory=Generic)

    defense: int = 200
    mitigation: float = 1.0
    regain: int = 100
    dodge_odds: float = 0.05
    effect_resistance: float = 0.05

    vitality: float = 1.0
    action_points: int = 0
    damage_taken: int = 0
    damage_dealt: int = 0
    kills: int = 0

    last_damage_taken: int = 0

    passives: list[str] = field(default_factory=list)
    dots: list[str] = field(default_factory=list)
    hots: list[str] = field(default_factory=list)
    damage_types: list[str] = field(default_factory=list)

    def apply_damage(self, amount: int) -> None:
        self.last_damage_taken = amount
        self.damage_taken += amount
        self.hp = max(self.hp - amount, 0)

    def apply_healing(self, amount: int) -> None:
        self.hp = min(self.hp + amount, self.max_hp)


StatusHook = Callable[["Stats"], None]
STATUS_HOOKS: list[StatusHook] = []


def add_status_hook(hook: StatusHook) -> None:
    STATUS_HOOKS.append(hook)


def apply_status_hooks(stats: "Stats") -> None:
    for hook in STATUS_HOOKS:
        hook(stats)

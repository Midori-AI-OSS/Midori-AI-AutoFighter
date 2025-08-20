from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from autofighter.stats import Stats
from autofighter.character import CharacterType
from plugins.damage_types.generic import Generic
from plugins.damage_types._base import DamageTypeBase


@dataclass
class FoeBase(Stats):
    plugin_type = "foe"

    hp: int = 1000
    max_hp: int = 1000
    atk: int = 100
    defense: int = 50
    gold: int = 1
    char_type: CharacterType = CharacterType.C
    prompt: str = "Foe prompt placeholder"
    about: str = "Foe description placeholder"

    exp: int = 1
    level: int = 1
    exp_multiplier: float = 1.0
    actions_per_turn: int = 1

    crit_rate: float = 0.05
    crit_damage: float = 2
    effect_hit_rate: float = 0.01
    base_damage_type: DamageTypeBase = field(default_factory=Generic)

    mitigation: int = 100
    regain: int = 1
    dodge_odds: float = 0
    effect_resistance: float = 1.0

    vitality: float = 1.0
    action_points: int = 1
    damage_taken: int = 1
    damage_dealt: int = 1
    kills: int = 1

    last_damage_taken: int = 1

    passives: list[str] = field(default_factory=list)
    dots: list[str] = field(default_factory=list)
    hots: list[str] = field(default_factory=list)
    damage_types: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.damage_types = [getattr(self.base_damage_type, "id", str(self.base_damage_type))]

    async def maybe_regain(self, turn: int) -> None:  # noqa: D401
        """Regain a fraction of HP every other turn."""
        if turn % 2 != 0:
            return
        bonus = max(self.regain - 100, 0) * 0.00005
        percent = (0.01 + bonus) / 100
        heal = int(self.max_hp * percent)
        await self.apply_healing(heal)

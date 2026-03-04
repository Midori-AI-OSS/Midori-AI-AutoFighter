from __future__ import annotations

import copy
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
import logging

from autofighter.character import CharacterType
from autofighter.stat_effect import StatEffect
from autofighter.stats import BUS
from autofighter.stats import Stats
from plugins.damage_types import random_damage_type
from plugins.damage_types._base import DamageTypeBase

# Supported foe rank values for upcoming features
SUPPORTED_RANKS = (
    "normal",
    "prime",
    "glitched prime",
    "boss",
    "glitched boss",
)

log = logging.getLogger(__name__)


@dataclass
class FoeBase(Stats):
    plugin_type = "foe"

    hp: int = 1000
    base_max_hp: int = 1000
    base_atk: int = 100
    base_defense: int = 50
    base_crit_rate: float = 0.05
    base_crit_damage: float = 2.0
    base_effect_hit_rate: float = 0.01
    base_mitigation: float = 0.001
    base_regain: int = 1
    base_dodge_odds: float = 0.0
    base_effect_resistance: float = 0.05
    base_vitality: float = 0.001

    gold: int = 1
    char_type: CharacterType = CharacterType.C
    prompt: str = "Foe prompt placeholder"
    about: str = "Foe description placeholder"
    voice_sample: str | None = None
    voice_gender: str | None = None

    exp: int = 1
    level: int = 1
    exp_multiplier: float = 1.0
    actions_per_turn: int = 1

    damage_type: DamageTypeBase = field(default_factory=random_damage_type)

    action_points: int = 0
    damage_taken: int = 1
    damage_dealt: int = 1
    kills: int = 1

    last_damage_taken: int = 1

    # Encounter rank indicating foe difficulty
    rank: str = "normal"

    passives: list[str] = field(default_factory=list)
    dots: list[str] = field(default_factory=list)
    hots: list[str] = field(default_factory=list)
    special_abilities: list[str] = field(default_factory=list)

    stat_gain_map: dict[str, str] = field(default_factory=dict)
    stat_loss_map: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.voice_gender is None:
            self.voice_gender = {
                CharacterType.A: "male",
                CharacterType.B: "female",
                CharacterType.C: "neutral",
            }.get(self.char_type)

        # Push the configured base stats into Stats' backing fields so that the
        # standard property accessors (used by scaling and combat systems) take
        # effect.
        _base_overrides: dict[str, float | int] = {
            "max_hp": self.base_max_hp,
            "atk": self.base_atk,
            "defense": self.base_defense,
            "crit_rate": self.base_crit_rate,
            "crit_damage": self.base_crit_damage,
            "effect_hit_rate": self.base_effect_hit_rate,
            "mitigation": self.base_mitigation,
            "regain": self.base_regain,
            "dodge_odds": self.base_dodge_odds,
            "effect_resistance": self.base_effect_resistance,
            "vitality": self.base_vitality,
        }
        for stat_name, value in _base_overrides.items():
            if isinstance(value, (int, float)):
                self.set_base_stat(stat_name, value)

        super().__post_init__()

    def __deepcopy__(self, memo):  # type: ignore[override]
        """Custom deepcopy preserving mutable dataclass field isolation."""
        cls = type(self)
        result = cls.__new__(cls)
        memo[id(self)] = result
        for f in fields(cls):
            val = getattr(self, f.name)
            setattr(result, f.name, copy.deepcopy(val, memo))
        return result

    async def use_ultimate(self) -> bool:
        """Consume charge and emit an event when firing the ultimate."""
        if not getattr(self, "ultimate_ready", False):
            return False
        self.ultimate_charge = 0
        self.ultimate_ready = False
        await BUS.emit_async("ultimate_used", self)
        return True

    async def maybe_regain(self, turn: int) -> None:
        """Regain a fraction of HP every other turn."""
        if turn % 2 != 0:
            return
        bonus = max(self.regain - 100, 0) * 0.00005
        percent = (0.01 + bonus) / 100
        heal = int(self.max_hp * percent)
        log.debug(
            "%s regains %s HP on turn %s",
            getattr(self, "id", type(self).__name__),
            heal,
            turn,
        )
        await self.apply_healing(heal)

    def _on_level_up(self) -> None:
        """Apply base bonuses then boost mitigation and vitality."""
        log.info(
            "%s leveled up to %s",
            getattr(self, "id", type(self).__name__),
            self.level + 1,
        )
        super()._on_level_up()
        self.add_effect(
            StatEffect(
                name="level_up_mitigation",
                stat_modifiers={"mitigation": 0.0001},
                source="level_up",
            )
        )
        self.add_effect(
            StatEffect(
                name="level_up_vitality",
                stat_modifiers={"vitality": 0.0001},
                source="level_up",
            )
        )

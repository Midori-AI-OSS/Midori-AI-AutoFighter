from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field

from game.actors import CharacterType

@dataclass
class Stats:
    """Basic combat statistics shared by players and foes."""

    hp: int
    max_hp: int
    atk: int = 0
    defense: int = 0
    gold: int = 0
    char_type: CharacterType = CharacterType.C

    # Core
    exp: int = 0
    level: int = 1
    exp_multiplier: float = 1.0
    actions_per_turn: int = 1

    # Offense
    crit_rate: float = 0.0
    crit_damage: float = 0.0
    effect_hit_rate: float = 0.0
    base_damage_type: str = "Generic"

    # Defense
    mitigation: int = 0
    regain: int = 0
    dodge_odds: float = 0.0
    effect_resistance: float = 0.0

    # Vitality & Advanced
    vitality: float = 0.0
    action_points: int = 0
    damage_taken: int = 0
    damage_dealt: int = 0
    kills: int = 0

    last_damage_taken: int = 0

    stunned: bool = False

    # Status lists
    passives: list[str] = field(default_factory=list)
    dots: list[str] = field(default_factory=list)
    hots: list[str] = field(default_factory=list)
    damage_types: list[str] = field(default_factory=lambda: ["Generic"])
    relics: list[str] = field(default_factory=list)

    def apply_damage(self, amount: int) -> None:
        """Reduce HP by ``amount`` without going below zero."""
        self.last_damage_taken = amount
        self.damage_taken += amount
        self.hp = max(self.hp - amount, 0)

    def apply_healing(self, amount: int) -> None:
        """Increase HP by ``amount`` without exceeding ``max_hp``."""
        self.hp = min(self.hp + amount, self.max_hp)

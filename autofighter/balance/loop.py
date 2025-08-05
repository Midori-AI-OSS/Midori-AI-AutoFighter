from __future__ import annotations

from dataclasses import dataclass

from autofighter.stats import Stats


@dataclass
class LoopConfig:
    """Tuning knobs for loop-based foe scaling."""

    base_multiplier: float = 1.2
    floor_boss_base: int = 100


config = LoopConfig()


def scale_stats(base: Stats, floor: int, room: int, loop: int, *, floor_boss: bool = False) -> Stats:
    """Return new stats scaled by floor, room, loop, and boss type."""
    loop = max(1, loop)
    factor = floor * room * loop
    if floor_boss:
        factor *= config.floor_boss_base
    factor *= config.base_multiplier ** (loop - 1)
    return Stats(
        hp=int(base.hp * factor),
        max_hp=int(base.max_hp * factor),
        atk=int(base.atk * factor),
        defense=int(base.defense * factor),
    )

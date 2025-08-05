"""Pressure level modifiers for enemy scaling."""

from __future__ import annotations

from autofighter.stats import Stats


def apply_pressure(base: Stats, pressure: int) -> Stats:
    """Return new stats scaled by pressure level."""
    multiplier = 1 + 0.05 * pressure
    return Stats(
        hp=int(base.hp * multiplier),
        max_hp=int(base.max_hp * multiplier),
        atk=int(base.atk * multiplier),
        defense=int(base.defense * multiplier),
    )

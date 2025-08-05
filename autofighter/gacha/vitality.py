from __future__ import annotations


def vitality_bonus(stacks: int) -> float:
    """Return total Vitality bonus for ``stacks`` duplicates."""

    bonus = 0.0
    increment = 0.0001
    for _ in range(stacks):
        bonus += increment
        increment *= 1.05
    return bonus

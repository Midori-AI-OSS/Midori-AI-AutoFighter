from __future__ import annotations

BASE_BONUS = 0.0001
BONUS_MULTIPLIER = 1.05


def stack_character(name: str, stacks: dict[str, int]) -> tuple[int, float]:
    """Increment stack count for ``name`` and return new count and bonus.

    Parameters
    ----------
    name:
        Character identifier.
    stacks:
        Mapping of character names to counts. Modified in place.

    Returns
    -------
    tuple[int, float]
        New stack count and Vitality bonus increment.
    """
    count = stacks.get(name, 0) + 1
    stacks[name] = count
    if count > 1:
        bonus = BASE_BONUS * (BONUS_MULTIPLIER ** (count - 2))
    else:
        bonus = 0.0
    return count, bonus


def total_bonus(count: int) -> float:
    """Return total Vitality bonus for ``count`` stacks."""
    if count <= 1:
        return 0.0
    return BASE_BONUS * (BONUS_MULTIPLIER ** (count - 1) - 1) / (BONUS_MULTIPLIER - 1)

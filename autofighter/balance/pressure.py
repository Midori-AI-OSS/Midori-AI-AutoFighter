from __future__ import annotations


def stat_multiplier(pressure: int) -> float:
    """Return the multiplier applied to enemy stats for a pressure level."""

    return 1 + 0.05 * pressure


def reward_multiplier(pressure: int) -> float:
    """Return the multiplier applied to rewards for a pressure level."""

    return 1 + 0.1 * pressure


def mechanic_bonus(pressure: int) -> float:
    """Return the additive mechanic bonus for a pressure level."""

    return 0.05 * pressure

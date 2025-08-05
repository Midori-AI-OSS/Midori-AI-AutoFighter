from __future__ import annotations

from autofighter.stats import Stats

from .pressure import mechanic_bonus
from .pressure import reward_multiplier
from .pressure import stat_multiplier


def scale_stats(base: Stats, loop: int, pressure: int) -> Stats:
    """Scale base stats for a floor boss."""

    factor = 100 * stat_multiplier(pressure) * (1.2 ** loop)
    return Stats(
        hp=int(base.hp * factor),
        max_hp=int(base.max_hp * factor),
        atk=int(base.atk * factor),
        defense=int(base.defense * factor),
    )


def scale_mechanics(loop: int, pressure: int) -> dict[str, float]:
    """Return mechanic modifiers for the boss."""

    return {
        "attack_bonus": mechanic_bonus(pressure) + 0.1 * loop,
        "extra_actions": loop // 2,
    }


def scale_rewards(base_gold: int, loop: int, pressure: int) -> dict[str, int]:
    """Scale gold and ticket rewards for defeating the boss."""

    gold = int(base_gold * (2 + 0.5 * loop) * reward_multiplier(pressure))
    tickets = min(5, 1 + pressure // 20 + loop)
    return {"gold": gold, "tickets": tickets}

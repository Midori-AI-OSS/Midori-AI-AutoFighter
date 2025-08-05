from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from typing import List


@dataclass
class BossInfo:
    """Configuration for a boss encounter."""

    attacks: List[int]
    reward: Dict[str, int | List[str]]
    model: str
    music: str


BOSS_PATTERNS: Dict[str, BossInfo] = {
    "demo": BossInfo(
        attacks=[5, 15, 25],
        reward={"gold": 100, "items": ["Demo Relic"]},
        model="cube",
        music="boss_theme",
    )
}


def get_boss_info(name: str) -> BossInfo:
    """Return boss pattern info by name, falling back to demo."""

    return BOSS_PATTERNS.get(name, BOSS_PATTERNS["demo"])

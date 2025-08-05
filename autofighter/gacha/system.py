from __future__ import annotations

import json
import random

from typing import Any
from typing import Dict
from typing import List
from dataclasses import field
from dataclasses import dataclass

from .vitality import vitality_bonus
from plugins.plugin_loader import PluginLoader


DEFAULT_BASE_RATE = 0.00001
DEFAULT_SOFT_PITY = 159
DEFAULT_HARD_PITY = 180


@dataclass
class GachaResult:
    """Container for pull outcomes."""

    characters: List[str] = field(default_factory=list)
    upgrade_items: int = 0
    vitality: Dict[str, float] = field(default_factory=dict)


class GachaSystem:
    """Handle gacha pulls and persistence."""

    def __init__(
        self,
        player_dir: str = "plugins/players",
        rng: random.Random | None = None,
        base_rate: float = DEFAULT_BASE_RATE,
        soft_pity: int = DEFAULT_SOFT_PITY,
        hard_pity: int = DEFAULT_HARD_PITY,
    ) -> None:
        self.rng = rng or random.Random()
        self.owned: Dict[str, int] = {}
        self.base_rate = base_rate
        self.soft_pity = soft_pity
        self.hard_pity = hard_pity
        self.pity_counter = 0

        loader = PluginLoader()
        loader.discover(player_dir)
        self.pool = list(loader.get_plugins("player").keys())

    def pull(self, count: int) -> GachaResult:
        if count not in (1, 5, 10):
            raise ValueError("count must be 1, 5, or 10")

        result = GachaResult()
        for _ in range(count):
            rate = self.current_rate()
            if self.rng.random() < rate:
                character = self.rng.choice(self.pool)
                stacks = self.owned.get(character, 0)
                self.owned[character] = stacks + 1
                result.characters.append(character)
                self.pity_counter = 0
                if stacks:
                    result.vitality[character] = vitality_bonus(stacks)
            else:
                result.upgrade_items += 1
                self.pity_counter += 1
        return result

    def serialize(self) -> str:
        return json.dumps(
            {
                "owned": self.owned,
                "pity": self.pity_counter,
                "base_rate": self.base_rate,
                "soft_pity": self.soft_pity,
                "hard_pity": self.hard_pity,
            }
        )

    @classmethod
    def deserialize(
        cls,
        data: str,
        player_dir: str = "plugins/players",
        rng: random.Random | None = None,
    ) -> "GachaSystem":
        payload: Dict[str, Any] = json.loads(data)
        obj = cls(
            player_dir=player_dir,
            rng=rng,
            base_rate=float(payload.get("base_rate", DEFAULT_BASE_RATE)),
            soft_pity=int(payload.get("soft_pity", DEFAULT_SOFT_PITY)),
            hard_pity=int(payload.get("hard_pity", DEFAULT_HARD_PITY)),
        )
        obj.owned = {str(k): int(v) for k, v in payload.get("owned", {}).items()}
        obj.pity_counter = int(payload.get("pity", 0))
        return obj

    def current_rate(self) -> float:
        pity = self.pity_counter + 1
        if pity >= self.hard_pity:
            return 1.0
        if pity <= self.soft_pity:
            return self.base_rate
        span = self.hard_pity - self.soft_pity
        progress = pity - self.soft_pity
        return self.base_rate + (1 - self.base_rate) * (progress / span)

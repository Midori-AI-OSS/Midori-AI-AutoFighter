from __future__ import annotations

import json
import random
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict
from typing import List

from plugins.plugin_loader import PluginLoader

from .vitality import vitality_bonus


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
    ) -> None:
        self.rng = rng or random.Random()
        self.owned: Dict[str, int] = {}

        loader = PluginLoader()
        loader.discover(player_dir)
        self.pool = list(loader.get_plugins("player").keys())

    def pull(self, count: int) -> GachaResult:
        if count not in (1, 5, 10):
            raise ValueError("count must be 1, 5, or 10")

        result = GachaResult()
        for _ in range(count):
            if self.rng.random() < 0.5:
                character = self.rng.choice(self.pool)
                stacks = self.owned.get(character, 0)
                self.owned[character] = stacks + 1
                result.characters.append(character)
                if stacks:
                    result.vitality[character] = vitality_bonus(stacks)
            else:
                result.upgrade_items += 1
        return result

    def serialize(self) -> str:
        return json.dumps({"owned": self.owned})

    @classmethod
    def deserialize(
        cls,
        data: str,
        player_dir: str = "plugins/players",
        rng: random.Random | None = None,
    ) -> "GachaSystem":
        obj = cls(player_dir=player_dir, rng=rng)
        payload: Dict[str, Any] = json.loads(data)
        obj.owned = {str(k): int(v) for k, v in payload.get("owned", {}).items()}
        return obj

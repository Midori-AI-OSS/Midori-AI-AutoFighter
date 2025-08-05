from __future__ import annotations

import json
import random

from typing import Any
from typing import Dict
from typing import List
from .crafting import craft_upgrades
from .crafting import trade_for_tickets
from .vitality import vitality_bonus
from dataclasses import dataclass
from dataclasses import field
from plugins.plugin_loader import PluginLoader


@dataclass
class GachaResult:
    """Container for pull outcomes."""

    characters: List[str] = field(default_factory=list)
    upgrade_items: Dict[int, int] = field(
        default_factory=lambda: {1: 0, 2: 0, 3: 0, 4: 0}
    )
    tickets: int = 0
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
        self.upgrade_items: Dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}
        self.tickets = 0

        loader = PluginLoader()
        loader.discover(player_dir)
        self.pool = list(loader.get_plugins("player").keys())

    def pull(self, count: int) -> GachaResult:
        if count not in (1, 5, 10):
            raise ValueError("count must be 1, 5, or 10")

        before = self.upgrade_items.copy()
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
                self.upgrade_items[1] += 1

        craft_upgrades(self.upgrade_items)
        tickets = trade_for_tickets(self.upgrade_items)
        self.tickets += tickets
        result.tickets = tickets

        for star in (1, 2, 3, 4):
            gained = self.upgrade_items.get(star, 0) - before.get(star, 0)
            if gained > 0:
                result.upgrade_items[star] = gained
        return result

    def serialize(self) -> str:
        return json.dumps(
            {
                "owned": self.owned,
                "upgrade_items": self.upgrade_items,
                "tickets": self.tickets,
            }
        )

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
        obj.upgrade_items = {
            int(k): int(v) for k, v in payload.get("upgrade_items", {}).items()
        }
        obj.tickets = int(payload.get("tickets", 0))
        return obj

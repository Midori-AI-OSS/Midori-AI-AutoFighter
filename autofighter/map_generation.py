"""Map generation utilities for building floor layouts.

Generates deterministic room sequences with required shop and rest
stops plus optional chat rooms. Pressure level raises room count,
adds branches and bonus bosses, and foe scaling respects floor,
room, and loop count.
"""

from __future__ import annotations

import json
import random
import importlib

from typing import List
from typing import Type
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class MapNode:
    """Single room on the run map."""

    index: int
    room_type: str
    links: List[int] = field(default_factory=list)
    chat_after: bool = False
    enemy_scale: float = 1.0


def _load_used_seeds(path: Path) -> set[int]:
    if not path.exists():
        return set()
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError:
        return set()
    return {int(x) for x in data}


def _save_used_seeds(seeds: set[int], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(sorted(seeds), fh)


class MapGenerator:
    """Builds floor maps with seeded randomness."""

    def __init__(
        self,
        base_seed: int,
        pressure_level: int = 0,
        loop: int = 0,
        seed_store_path: Path | str | None = None,
    ) -> None:
        self.base_seed = base_seed
        self.pressure_level = pressure_level
        self.loop = loop
        self.seed_store_path = Path(seed_store_path) if seed_store_path else Path("used_seeds.json")
        used = _load_used_seeds(self.seed_store_path)
        if base_seed in used:
            raise ValueError(f"base seed {base_seed} already used")
        used.add(base_seed)
        _save_used_seeds(used, self.seed_store_path)

    def _rng(self, floor: int) -> random.Random:
        return random.Random(self.base_seed + floor)

    def generate_floor(self, floor: int) -> List[MapNode]:
        rng = self._rng(floor)
        extra_rooms = self.pressure_level // 10
        total_rooms = 45 + extra_rooms
        extra_bosses = self.pressure_level // 20
        branch_count = min(self.pressure_level // 15, total_rooms - 2)

        # Preselect shop and rest positions (exclude final rooms)
        available = list(range(1, total_rooms - 1))
        shop_positions = set(rng.sample(available, k=2))
        remaining = [i for i in available if i not in shop_positions]
        rest_positions = set(rng.sample(remaining, k=2))
        remaining = [i for i in remaining if i not in rest_positions]

        # Place extra bosses across the map
        boss_positions = set()
        if extra_bosses:
            boss_positions = set(rng.sample(remaining, k=extra_bosses))

        # Branch positions skip ahead one room
        branch_positions = set()
        if branch_count:
            branch_positions = set(rng.sample(range(1, total_rooms - 2), k=branch_count))

        nodes: List[MapNode] = []
        for idx in range(total_rooms):
            if idx == total_rooms - 1:
                room_type = "battle_boss_floor"
            elif idx in boss_positions:
                room_type = "battle_boss"
            elif idx in shop_positions:
                room_type = "shop"
            elif idx in rest_positions:
                room_type = "rest"
            else:
                room_type = rng.choice(["battle_normal", "battle_weak"])

            chat_after = room_type.startswith("battle") and rng.random() < 0.3
            scale = (floor * (idx + 1))
            scale *= 1.2 ** self.loop
            scale *= rng.uniform(0.95, 1.05)
            nodes.append(
                MapNode(
                    index=idx,
                    room_type=room_type,
                    chat_after=chat_after,
                    enemy_scale=scale,
                )
            )

            if idx + 1 < total_rooms:
                nodes[-1].links.append(idx + 1)
                if idx in branch_positions:
                    nodes[-1].links.append(idx + 2)

        if len(nodes) >= 5:
            nodes[0].links = [1, 2, 3]
            nodes[1].links = [4]
            nodes[2].links = [4]
            nodes[3].links = [4]

        return nodes


def render_floor(nodes: List[MapNode]) -> str:
    """Return a simple vertical map representation."""

    symbols = {
        "battle_weak": "BW",
        "battle_normal": "BN",
        "battle_boss": "BB",
        "battle_boss_floor": "FB",
        "shop": "SH",
        "rest": "RR",
    }
    lines = []
    for node in nodes:
        sym = symbols.get(node.room_type, "??")
        chat = " *" if node.chat_after else ""
        if node.links:
            links = ",".join(f"{i:02d}" for i in node.links)
            lines.append(f"{node.index:02d}:{sym} -> {links}{chat}")
        else:
            lines.append(f"{node.index:02d}:{sym}{chat}")
    return "\n".join(lines)


ROOM_MODULES = {
    "battle_weak": "autofighter.battle_room.BattleRoom",
    "battle_normal": "autofighter.battle_room.BattleRoom",
    "battle_boss": "autofighter.rooms.boss_room.BossRoom",
    "battle_boss_floor": "autofighter.rooms.boss_room.BossRoom",
    "shop": "autofighter.shop_room.ShopRoom",
    "rest": "autofighter.rest_room.RestRoom",
    "event": "autofighter.event_room.EventRoom",
}


def load_room_class(room_type: str) -> Type[object]:
    """Import and return the class for a given room type."""

    target = ROOM_MODULES[room_type]
    module_name, class_name = target.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

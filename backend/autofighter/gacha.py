from __future__ import annotations

import json
import random

from dataclasses import dataclass
from typing import Any

from plugins import players as player_plugins
from plugins.damage_types import ALL_DAMAGE_TYPES

from .save_manager import SaveManager


def _build_pools() -> tuple[list[str], list[str]]:
    five: list[str] = []
    six: list[str] = []
    for name in getattr(player_plugins, "__all__", []):
        cls = getattr(player_plugins, name)
        rarity = getattr(cls, "gacha_rarity", 0)
        cid = getattr(cls, "id", name)
        if cid in {"player", "luna"}:
            continue
        if rarity == 5:
            five.append(cid)
        elif rarity == 6:
            six.append(cid)
    return five, six


FIVE_STAR, SIX_STAR = _build_pools()
ELEMENTS = [e.lower() for e in ALL_DAMAGE_TYPES]


@dataclass
class PullResult:
    type: str
    id: str
    rarity: int
    stacks: int | None = None


class GachaManager:
    def __init__(self, save: SaveManager) -> None:
        self.save = save
        with self.save.connection() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS player_stacks (id TEXT PRIMARY KEY, stacks INTEGER NOT NULL)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, value TEXT)"
            )

    def _get_pity(self) -> int:
        with self.save.connection() as conn:
            cur = conn.execute(
                "SELECT value FROM options WHERE key = ?", ("gacha_pity",)
            )
            row = cur.fetchone()
            return int(row[0]) if row else 0

    def _set_pity(self, value: int) -> None:
        with self.save.connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO options (key, value) VALUES (?, ?)",
                ("gacha_pity", str(value)),
            )

    def _get_items(self) -> dict[str, int]:
        with self.save.connection() as conn:
            cur = conn.execute(
                "SELECT value FROM options WHERE key = ?", ("upgrade_items",)
            )
            row = cur.fetchone()
            if row:
                try:
                    data = json.loads(row[0])
                    if isinstance(data, dict):
                        return {str(k): int(v) for k, v in data.items()}
                except json.JSONDecodeError:
                    pass
            return {}

    def _set_items(self, items: dict[str, int]) -> None:
        with self.save.connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO options (key, value) VALUES (?, ?)",
                ("upgrade_items", json.dumps(items)),
            )

    def _get_auto_craft(self) -> bool:
        with self.save.connection() as conn:
            cur = conn.execute(
                "SELECT value FROM options WHERE key = ?", ("auto_craft",)
            )
            row = cur.fetchone()
            return bool(int(row[0])) if row else False

    def _set_auto_craft(self, enabled: bool) -> None:
        with self.save.connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO options (key, value) VALUES (?, ?)",
                ("auto_craft", "1" if enabled else "0"),
            )

    def _auto_craft(self, items: dict[str, int]) -> None:
        for element in ELEMENTS:
            for star in (1, 2, 3):
                lower = f"{element}_{star}"
                higher = f"{element}_{star + 1}"
                while items.get(lower, 0) >= 125:
                    items[lower] -= 125
                    items[higher] = items.get(higher, 0) + 1
            while items.get(f"{element}_4", 0) >= 10:
                items[f"{element}_4"] -= 10
                items["ticket"] = items.get("ticket", 0) + 1

    def _add_character(self, cid: str) -> int:
        with self.save.connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO owned_players (id) VALUES (?)",
                (cid,),
            )
            cur = conn.execute(
                "SELECT stacks FROM player_stacks WHERE id = ?", (cid,)
            )
            row = cur.fetchone()
            stacks = int(row[0]) + 1 if row else 1
            conn.execute(
                "INSERT OR REPLACE INTO player_stacks (id, stacks) VALUES (?, ?)",
                (cid, stacks),
            )
        return stacks

    def _get_owned(self) -> set[str]:
        with self.save.connection() as conn:
            cur = conn.execute("SELECT id FROM owned_players")
            return {row[0] for row in cur.fetchall()}

    def _rarity_weights(self, pity: int) -> list[float]:
        factor = min(pity, 180) / 180
        return [
            0.10 * (1 - factor),
            0.50 - 0.20 * factor,
            0.30 + 0.20 * factor,
            0.10 + 0.10 * factor,
        ]

    def pull(self, count: int) -> list[PullResult]:
        if count not in (1, 5, 10):
            raise ValueError("invalid pull count")
        results: list[PullResult] = []
        pity = self._get_pity()
        items = self._get_items()
        owned = self._get_owned()
        auto_craft = self._get_auto_craft()
        for _ in range(count):
            if random.random() < 0.0001:
                pool = [c for c in SIX_STAR if c not in owned]
                cid = random.choice(pool or SIX_STAR)
                stacks = self._add_character(cid)
                owned.add(cid)
                results.append(PullResult("character", cid, 6, stacks))
                pity = 0
                continue
            pity_chance = 0.00001 + pity * ((0.05 - 0.00001) / 159)
            if pity >= 179 or random.random() < pity_chance:
                pool = [c for c in FIVE_STAR if c not in owned]
                cid = random.choice(pool or FIVE_STAR)
                stacks = self._add_character(cid)
                owned.add(cid)
                results.append(PullResult("character", cid, 5, stacks))
                pity = 0
            else:
                weights = self._rarity_weights(pity)
                roll = random.random()
                threshold = 0.0
                rarity = 1
                for idx, weight in enumerate(weights, start=1):
                    threshold += weight
                    if roll < threshold:
                        rarity = idx
                        break
                element = random.choice(ELEMENTS)
                key = f"{element}_{rarity}"
                items[key] = items.get(key, 0) + 1
                if auto_craft:
                    self._auto_craft(items)
                results.append(PullResult("item", key, rarity))
                pity += 1
        self._set_pity(pity)
        self._set_items(items)
        return results

    def get_state(self) -> dict[str, Any]:
        pity = self._get_pity()
        items = self._get_items()
        auto_craft = self._get_auto_craft()
        with self.save.connection() as conn:
            cur = conn.execute(
                "SELECT p.id, COALESCE(s.stacks, 0) FROM owned_players p LEFT JOIN player_stacks s ON p.id = s.id"
            )
            players = [
                {"id": row[0], "stacks": row[1]} for row in cur.fetchall()
            ]
        return {
            "pity": pity,
            "items": items,
            "players": players,
            "auto_craft": auto_craft,
        }

    def set_auto_craft(self, enabled: bool) -> None:
        self._set_auto_craft(enabled)

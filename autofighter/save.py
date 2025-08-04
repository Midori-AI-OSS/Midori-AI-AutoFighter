from __future__ import annotations

import json
from pathlib import Path

from autofighter.stats import Stats

PLAYER_FILE = Path("player.json")


def save_player(body: str, hair: str, hair_color: str, accessory: str, stats: Stats) -> None:
    data = {
        "body": body,
        "hair": hair,
        "hair_color": hair_color,
        "accessory": accessory,
        "stats": stats.__dict__,
    }
    PLAYER_FILE.write_text(json.dumps(data))


def load_player() -> tuple[str, str, str, str, Stats] | None:
    if not PLAYER_FILE.exists():
        return None
    data = json.loads(PLAYER_FILE.read_text())
    stats_data = data.get("stats", {})
    stats = Stats(**stats_data)
    return (
        data.get("body", "Athletic"),
        data.get("hair", "Short"),
        data.get("hair_color", "Black"),
        data.get("accessory", "None"),
        stats,
    )

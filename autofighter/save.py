from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from autofighter.saves import SaveManager
from autofighter.stats import Stats

DB_PATH = Path("save.db")
SETTINGS_PATH = Path("settings.json")
DEFAULT_SETTINGS: dict[str, Any] = {
    "sfx_volume": 0.5,
    "music_volume": 0.5,
    "stat_refresh_rate": 5,
    "pause_on_stats": True,
}


def load_settings(path: Path | None = None) -> dict[str, Any]:
    path = path or SETTINGS_PATH
    if path.exists():
        try:
            data = json.loads(path.read_text())
            return {**DEFAULT_SETTINGS, **data}
        except Exception:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict[str, Any], path: Path | None = None) -> None:
    path = path or SETTINGS_PATH
    path.write_text(json.dumps(settings))


def load_run(source: Path | str, password: str = "", path: Path = DB_PATH) -> Stats | None:
    if isinstance(source, Path):
        if not source.exists():
            return None
        try:
            data = json.loads(source.read_text())
            stats_data = data.get("stats", {})
            return Stats(**stats_data)
        except Exception:
            return None
    with SaveManager(path, password) as sm:
        data = sm.fetch_run(source)
    if not data:
        return None
    stats_data = data.get("stats", {})
    return Stats(**stats_data)


def save_run(run_id: str, stats: Stats, password: str = "", path: Path = DB_PATH) -> None:
    payload = {"stats": stats.__dict__}
    with SaveManager(path, password) as sm:
        sm.queue_run(run_id, payload)
        sm.commit()


def save_player(
    body: str,
    hair: str,
    hair_color: str,
    accessory: str,
    stats: Stats,
    inventory: dict[str, int],
    password: str = "",
    path: Path = DB_PATH,
    player_id: str = "player",
) -> None:
    data: dict[str, Any] = {
        "body": body,
        "hair": hair,
        "hair_color": hair_color,
        "accessory": accessory,
        "stats": stats.__dict__,
        "inventory": inventory,
    }
    with SaveManager(path, password) as sm:
        existing = sm.fetch_player(player_id) or {}
        if "roster" in existing:
            data["roster"] = existing["roster"]
        sm.queue_player(player_id, data)
        sm.commit()


def load_player(
    password: str = "",
    path: Path = DB_PATH,
    player_id: str = "player",
) -> tuple[str, str, str, str, Stats, dict[str, int]] | None:
    with SaveManager(path, password) as sm:
        data = sm.fetch_player(player_id)
    if not data:
        return None
    stats_data = data.get("stats", {})
    stats = Stats(**stats_data)
    return (
        data.get("body", "Athletic"),
        data.get("hair", "Short"),
        data.get("hair_color", "Black"),
        data.get("accessory", "None"),
        stats,
        data.get("inventory", {}),
    )


def save_roster(
    roster: list[str],
    password: str = "",
    path: Path = DB_PATH,
    player_id: str = "player",
) -> None:
    with SaveManager(path, password) as sm:
        data = sm.fetch_player(player_id) or {}
        data["roster"] = roster
        sm.queue_player(player_id, data)
        sm.commit()


def load_roster(
    password: str = "",
    path: Path = DB_PATH,
    player_id: str = "player",
) -> list[str]:
    with SaveManager(path, password) as sm:
        data = sm.fetch_player(player_id)
    if not data:
        return []
    roster = data.get("roster", [])
    return [str(c) for c in roster]

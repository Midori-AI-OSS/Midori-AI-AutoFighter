from __future__ import annotations

import json
from pathlib import Path

from autofighter.stats import Stats
from autofighter.save import PLAYER_FILE
from autofighter.gacha.duplicates import stack_character


def add_character(name: str, *, path: Path = PLAYER_FILE) -> float:
    """Add ``name`` to the player's roster and apply Vitality bonus.

    Parameters
    ----------
    name:
        Character identifier.
    path:
        Save file to modify. Defaults to :data:`~autofighter.save.PLAYER_FILE`.

    Returns
    -------
    float
        Vitality bonus applied from this addition.
    """
    data: dict[str, object] = {}
    if path.exists():
        data = json.loads(path.read_text())

    stacks: dict[str, int] = data.get("characters", {})
    _, bonus = stack_character(name, stacks)
    data["characters"] = stacks

    stats_data = data.get("stats") or {"hp": 0, "max_hp": 0}
    stats = Stats(**stats_data)
    stats.vitality += bonus
    data["stats"] = stats.__dict__

    path.write_text(json.dumps(data))
    return bonus

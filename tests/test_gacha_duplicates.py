from __future__ import annotations

import json
from pathlib import Path

from autofighter.gacha.system import add_character


def test_duplicate_stacking(tmp_path: Path) -> None:
    path = tmp_path / "player.json"
    data = {"stats": {"hp": 10, "max_hp": 10, "vitality": 0.0}}
    path.write_text(json.dumps(data))

    bonus = add_character("Becca", path=path)
    assert bonus == 0.0
    data = json.loads(path.read_text())
    assert data["characters"]["Becca"] == 1
    assert data["stats"]["vitality"] == 0.0

    bonus = add_character("Becca", path=path)
    assert bonus == 0.0001
    data = json.loads(path.read_text())
    assert data["characters"]["Becca"] == 2
    assert data["stats"]["vitality"] == 0.0001

    bonus = add_character("Becca", path=path)
    assert bonus == 0.000105
    data = json.loads(path.read_text())
    assert data["characters"]["Becca"] == 3
    assert data["stats"]["vitality"] == 0.000205

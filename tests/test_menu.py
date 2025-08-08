from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from shutil import copy

import pytest

pytest.importorskip("direct")
sys.modules["sqlcipher3"] = sqlite3
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

from autofighter.saves import SaveManager
from game.ui.menu import MainMenu


def _setup_temp_assets(tmp_path: Path) -> tuple[Path, Path]:
    db_path = tmp_path / "save.db"
    avatars_dir = tmp_path / "avatars"
    avatars_dir.mkdir()
    copy("assets/textures/players/player1.png", avatars_dir / "a.png")
    copy("assets/textures/players/player2.png", avatars_dir / "b.png")
    return db_path, avatars_dir


def test_main_menu_structure(tmp_path: Path) -> None:
    loadPrcFileData("", "window-type none")
    base = ShowBase()
    db_path, avatars_dir = _setup_temp_assets(tmp_path)
    menu = MainMenu(base.aspect2d, db_path=db_path, avatars_dir=avatars_dir)
    assert len(menu.icon_buttons) == 7
    assert menu.run_button["text"] == "Start Run"
    assert menu.top_bar.getParent() is menu.root
    assert menu.root.getParent() is base.aspect2d
    with SaveManager(db_path, "") as sm:
        data = sm.fetch_player("player") or {}
    assert Path(data["avatar"]).exists()
    base.destroy()


def test_run_button_label_switch(tmp_path: Path) -> None:
    loadPrcFileData("", "window-type none")
    base = ShowBase()
    db_path, avatars_dir = _setup_temp_assets(tmp_path)
    menu = MainMenu(
        base.aspect2d,
        has_run=True,
        db_path=db_path,
        avatars_dir=avatars_dir,
    )
    assert menu.run_button["text"] == "Load Run"
    base.destroy()

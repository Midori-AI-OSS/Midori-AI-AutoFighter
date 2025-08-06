import importlib

import pytest


def test_game_package_imports() -> None:
    for sub in ["actors", "ui", "rooms", "gacha", "saves"]:
        importlib.import_module(f"game.{sub}")


def test_missing_submodule_raises() -> None:
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("game.nonexistent")

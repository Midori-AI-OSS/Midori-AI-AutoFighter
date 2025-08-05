
import pytest

try:
    from panda3d.core import loadPrcFileData
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    pytest.skip("panda3d not installed", allow_module_level=True)
    
import sys
import importlib

from pathlib import Path

try:
    importlib.import_module("panda3d.core")
except ModuleNotFoundError:  # pragma: no cover - Panda3D missing
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

sys.path.append(str(Path(__file__).resolve().parents[1]))

from panda3d.core import loadPrcFileData

from main import AutoFighterApp


def test_placeholder_attached() -> None:
    loadPrcFileData("", "window-type none")
    app = AutoFighterApp()
    try:
        assert app._placeholder.get_parent() is app.render
    finally:
        app.userExit()


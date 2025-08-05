import pytest

try:
    from panda3d.core import loadPrcFileData
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    pytest.skip("panda3d not installed", allow_module_level=True)

from main import AutoFighterApp


def test_placeholder_attached() -> None:
    loadPrcFileData("", "window-type none")
    app = AutoFighterApp()
    try:
        assert app._placeholder.get_parent() is app.render
    finally:
        app.userExit()


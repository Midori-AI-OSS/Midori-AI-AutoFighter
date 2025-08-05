from panda3d.core import loadPrcFileData

from main import AutoFighterApp


def test_placeholder_attached() -> None:
    loadPrcFileData("", "window-type none")
    app = AutoFighterApp()
    try:
        assert app._placeholder.get_parent() is app.render
    finally:
        app.userExit()


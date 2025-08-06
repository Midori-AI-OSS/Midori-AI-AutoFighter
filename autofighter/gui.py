from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from direct.showbase.ShowBase import ShowBase

WIDGET_SCALE = 0.1
SLIDER_SCALE = WIDGET_SCALE * 3
FRAME_COLOR = (0, 0, 0, 0.6)
TEXT_COLOR = (1, 1, 1, 1)


def get_aspect(app: ShowBase | object) -> float:
    """Return the application's window aspect ratio."""
    if hasattr(app, "getAspectRatio"):
        try:
            return float(app.getAspectRatio())
        except Exception:
            pass
    if hasattr(app, "win"):
        try:
            w = app.win.getXSize()
            h = app.win.getYSize()
        except Exception:
            return 1.0
        return w / h if h else 1.0
    return 1.0


def scale_ui(app: ShowBase | object, value: float) -> float:
    """Scale a UI value based on the window aspect ratio."""
    aspect = get_aspect(app)
    return value / max(aspect, 1.0)


def set_widget_pos(widget, pos: tuple[float, float, float]) -> None:
    """Set widget position for both Panda3D and headless tests."""
    if hasattr(widget, "setPos"):
        widget.setPos(*pos)
    else:
        widget["pos"] = pos

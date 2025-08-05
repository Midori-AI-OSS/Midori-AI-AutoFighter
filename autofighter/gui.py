from __future__ import annotations


WIDGET_SCALE = 0.1


def set_widget_pos(widget, pos: tuple[float, float, float]) -> None:
    """Set widget position for both Panda3D and headless tests."""
    if hasattr(widget, "setPos"):
        widget.setPos(*pos)
    else:
        widget["pos"] = pos

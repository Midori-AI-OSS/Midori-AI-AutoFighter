from __future__ import annotations

from typing import Any
from typing import Callable

WIDGET_SCALE = 0.1
SLIDER_SCALE = WIDGET_SCALE * 3
FRAME_COLOR = (0, 0, 0, 0.6)
TEXT_COLOR = (1, 1, 1, 1)


def set_widget_pos(widget, pos: tuple[float, float, float]) -> None:
    """Set widget position for both Panda3D and headless tests."""
    if hasattr(widget, "setPos"):
        widget.setPos(*pos)
    else:
        widget["pos"] = pos


_RESPONSIVE_UPDATERS: list[Callable[[], None]] = []


def bind_responsive(
    app: Any,
    widget: Any,
    x_frac: float,
    z: float,
    scale: float = WIDGET_SCALE,
) -> None:
    """Bind ``widget`` to update with window size changes.

    ``x_frac`` is the horizontal position expressed as a fraction of the
    window's width, with ``-1`` being the far left and ``1`` the far right.
    ``z`` is the vertical coordinate in render2d space.
    """

    def update() -> None:
        try:
            width = app.win.getXSize()
            height = app.win.getYSize()
            aspect = width / height if height else 1.0
        except Exception:  # pragma: no cover - headless tests
            aspect = 1.0
        set_widget_pos(widget, (x_frac * aspect, 0, z))
        if hasattr(widget, "setScale"):
            widget.setScale(scale)
        else:
            widget["scale"] = scale

    _RESPONSIVE_UPDATERS.append(update)
    update()
    try:  # pragma: no cover - headless tests
        app.accept("window-event", lambda *_: [u() for u in _RESPONSIVE_UPDATERS])
    except Exception:
        pass


def clear_responsive() -> None:
    """Clear all responsive widget bindings."""
    _RESPONSIVE_UPDATERS.clear()

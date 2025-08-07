from __future__ import annotations

FRAME_COLOR = (0, 0, 0, 0.6)
TEXT_COLOR = (1, 1, 1, 1)

BASE_WIDTH = 1280
BASE_HEIGHT = 720
BASE_SCALE = 0.1


def _window_size() -> tuple[int, int]:
    win = getattr(globals().get("base"), "win", None)
    if win:
        try:
            return win.get_size()
        except Exception:
            props = win.get_properties()
            return props.get_x_size(), props.get_y_size()
    return BASE_WIDTH, BASE_HEIGHT


def get_widget_scale() -> float:
    """Return a scale that keeps widget size consistent across window sizes."""

    width, height = _window_size()
    width = width or BASE_WIDTH
    height = height or BASE_HEIGHT
    # Use the minimum scale to prevent horizontal stretching
    scale_w = width / BASE_WIDTH
    scale_h = height / BASE_HEIGHT
    scale = min(scale_w, scale_h)
    return BASE_SCALE * scale


def get_slider_scale() -> float:
    return get_widget_scale() * 3


def get_normalized_scale_pos(
    x: float,
    y: float,
    scale_multiplier: float = 1.0,
) -> tuple[float, tuple[float, float, float]]:
    width, height = _window_size()
    scale = get_widget_scale() * scale_multiplier
    pos = (x / width) * 2 - 1, 0, 1 - (y / height) * 2
    return scale, pos


def set_widget_pos(widget, pos: tuple[float, float, float]) -> None:
    """Set widget position for both Panda3D and headless tests."""
    if hasattr(widget, "setPos"):
        widget.setPos(*pos)
    else:
        widget["pos"] = pos

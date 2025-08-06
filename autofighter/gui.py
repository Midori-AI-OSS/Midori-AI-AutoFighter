from __future__ import annotations

FRAME_COLOR = (0, 0, 0, 0.6)
TEXT_COLOR = (1, 1, 1, 1)
_BASE_DPI = 96


def _window_size() -> tuple[int, int]:
    win = getattr(globals().get("base"), "win", None)
    if win:
        try:
            return win.get_size()
        except Exception:
            props = win.get_properties()
            return props.get_x_size(), props.get_y_size()
    return 800, 600


def get_widget_scale() -> float:
    width, height = _window_size()
    win = getattr(globals().get("base"), "win", None)
    dpi = _BASE_DPI
    if win:
        try:
            info = win.get_display_information()
            dpi = getattr(info, "get_pixels_per_display_unit", lambda: _BASE_DPI)() or _BASE_DPI
        except Exception:
            dpi = _BASE_DPI
    return min(width, height) / (dpi * 10)


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

import math

from autofighter import gui


def test_widget_scale_constant_pixels(monkeypatch):
    monkeypatch.setattr(gui, "_window_size", lambda: (800, 600))
    small = gui.get_widget_scale()
    monkeypatch.setattr(gui, "_window_size", lambda: (1920, 1080))
    large = gui.get_widget_scale()
    assert math.isclose(small * 600, large * 1080, rel_tol=1e-9)


def test_widget_scale_zero_height(monkeypatch):
    monkeypatch.setattr(gui, "_window_size", lambda: (800, 0))
    assert gui.get_widget_scale() == gui.BASE_SCALE

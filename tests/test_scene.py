import logging

from typing import Any

from autofighter.scene import SceneManager, Scene

class DummyScene(Scene):
    def __init__(self) -> None:
        self.setup_called = False
        self.teardown_called = False

    def setup(self) -> None:
        self.setup_called = True

    def teardown(self) -> None:
        self.teardown_called = True


class SetupErrorScene(Scene):
    def setup(self) -> None:
        raise RuntimeError("setup boom")


class TeardownErrorScene(Scene):
    def teardown(self) -> None:
        raise RuntimeError("teardown boom")


def test_switch_to_cleans_previous_scene() -> None:
    base = object()
    mgr = SceneManager(base)
    first = DummyScene()
    second = DummyScene()
    mgr.switch_to(first)
    mgr.switch_to(second)
    assert first.teardown_called
    assert second.setup_called
    assert mgr.current is second


def test_overlays_push_pop_and_switch_clear() -> None:
    base = object()
    mgr = SceneManager(base)
    main = DummyScene()
    overlay = DummyScene()
    mgr.switch_to(main)
    mgr.push_overlay(overlay)
    assert overlay.setup_called
    mgr.pop_overlay()
    assert overlay.teardown_called
    mgr.push_overlay(overlay)
    mgr.switch_to(DummyScene())
    assert overlay.teardown_called
    assert mgr.overlays == []


def test_switch_to_none_clears_overlays() -> None:
    base = object()
    mgr = SceneManager(base)
    main = DummyScene()
    overlay = DummyScene()
    mgr.switch_to(main)
    mgr.push_overlay(overlay)
    mgr.switch_to(None)
    assert main.teardown_called
    assert overlay.teardown_called
    assert mgr.current is None
    assert mgr.overlays == []


def test_switch_to_logs_setup_failure_and_skips_scene(caplog: Any) -> None:
    base = object()
    mgr = SceneManager(base)
    with caplog.at_level(logging.ERROR):
        mgr.switch_to(SetupErrorScene())
    assert mgr.current is None
    assert any("Error setting up scene" in r.message for r in caplog.records)


def test_switch_to_logs_teardown_failure_and_continues(caplog: Any) -> None:
    base = object()
    mgr = SceneManager(base)
    mgr.switch_to(TeardownErrorScene())
    good = DummyScene()
    with caplog.at_level(logging.ERROR):
        assert mgr.switch_to(good) is False
    assert good.setup_called
    assert good.teardown_called
    assert isinstance(mgr.current, TeardownErrorScene)
    assert any("Error tearing down scene" in r.message for r in caplog.records)


def test_overlay_setup_and_teardown_errors_logged(caplog: Any) -> None:
    base = object()
    mgr = SceneManager(base)
    with caplog.at_level(logging.ERROR):
        assert mgr.push_overlay(SetupErrorScene()) is False
    assert mgr.overlays == []
    assert any("Error preparing overlay" in r.message for r in caplog.records)
    caplog.clear()
    class BadOverlay(DummyScene):
        def teardown(self) -> None:  # type: ignore[override]
            raise RuntimeError("teardown boom")
    overlay = BadOverlay()
    assert mgr.push_overlay(overlay) is True
    with caplog.at_level(logging.ERROR):
        assert mgr.pop_overlay() is False
    assert mgr.overlays == [overlay]
    assert any("Error removing overlay" in r.message for r in caplog.records)

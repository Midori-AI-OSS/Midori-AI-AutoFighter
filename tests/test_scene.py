from autofighter.scene import SceneManager, Scene


class DummyScene(Scene):
    def __init__(self) -> None:
        self.setup_called = False
        self.teardown_called = False

    def setup(self) -> None:
        self.setup_called = True

    def teardown(self) -> None:
        self.teardown_called = True


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

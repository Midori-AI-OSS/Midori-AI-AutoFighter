import types

from autofighter.scene import Scene, SceneManager


class DummyScene(Scene):
    def __init__(self) -> None:
        self.calls = []

    def setup(self) -> None:  # type: ignore[override]
        self.calls.append("setup")

    def transition_in(self) -> None:  # type: ignore[override]
        self.calls.append("in")

    def transition_out(self) -> None:  # type: ignore[override]
        self.calls.append("out")

    def teardown(self) -> None:  # type: ignore[override]
        self.calls.append("teardown")


class BadSetupScene(Scene):
    def setup(self) -> None:  # type: ignore[override]
        raise RuntimeError


def test_switch_to_invokes_hooks() -> None:
    manager = SceneManager(types.SimpleNamespace())
    first = DummyScene()
    second = DummyScene()

    manager.switch_to(first)
    assert first.calls == ["setup", "in"]

    manager.switch_to(second)
    assert first.calls[-2:] == ["out", "teardown"]
    assert second.calls == ["setup", "in"]


def test_overlays_push_and_pop() -> None:
    manager = SceneManager(types.SimpleNamespace())
    overlay = DummyScene()

    manager.push_overlay(overlay)
    assert manager.overlays == [overlay]
    assert overlay.calls == ["setup", "in"]

    manager.pop_overlay()
    assert overlay.calls[-2:] == ["out", "teardown"]
    assert manager.overlays == []


def test_switch_clears_overlays() -> None:
    manager = SceneManager(types.SimpleNamespace())
    overlay = DummyScene()
    scene = DummyScene()

    manager.push_overlay(overlay)
    manager.switch_to(scene)
    assert overlay.calls == ["setup", "in", "out", "teardown"]
    assert manager.overlays == []
    assert manager.current is scene


def test_push_overlay_failure_does_not_register() -> None:
    manager = SceneManager(types.SimpleNamespace())
    bad = BadSetupScene()
    manager.push_overlay(bad)
    assert manager.overlays == []

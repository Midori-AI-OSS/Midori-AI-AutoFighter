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

    assert manager.switch_to(first) is True
    assert first.calls == ["setup", "in"]

    assert manager.switch_to(second) is True
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
    assert manager.switch_to(scene) is True
    assert overlay.calls == ["setup", "in", "out", "teardown"]
    assert manager.overlays == []
    assert manager.current is scene


def test_push_overlay_failure_does_not_register() -> None:
    manager = SceneManager(types.SimpleNamespace())
    bad = BadSetupScene()
    manager.push_overlay(bad)
    assert manager.overlays == []


def test_switch_failure_restores_previous_scene() -> None:
    manager = SceneManager(types.SimpleNamespace())
    good = DummyScene()
    bad = BadSetupScene()

    assert manager.switch_to(good) is True
    assert manager.current is good

    assert manager.switch_to(bad) is False
    assert manager.current is good

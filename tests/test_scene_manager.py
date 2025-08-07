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


class BadOutScene(DummyScene):
    def transition_out(self) -> None:  # type: ignore[override]
        raise RuntimeError


class BadOverlay(DummyScene):
    def transition_out(self) -> None:  # type: ignore[override]
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

    assert manager.push_overlay(overlay) is True
    assert manager.overlays == [overlay]
    assert overlay.calls == ["setup", "in"]

    assert manager.pop_overlay() is True
    assert overlay.calls[-2:] == ["out", "teardown"]
    assert manager.overlays == []


def test_switch_clears_overlays() -> None:
    manager = SceneManager(types.SimpleNamespace())
    overlay = DummyScene()
    scene = DummyScene()

    assert manager.push_overlay(overlay) is True
    assert manager.switch_to(scene) is True
    assert overlay.calls == ["setup", "in", "out", "teardown"]
    assert manager.overlays == []
    assert manager.current is scene


def test_push_overlay_failure_does_not_register() -> None:
    manager = SceneManager(types.SimpleNamespace())
    bad = BadSetupScene()
    assert manager.push_overlay(bad) is False
    assert manager.overlays == []


def test_switch_failure_restores_previous_scene() -> None:
    manager = SceneManager(types.SimpleNamespace())
    good = DummyScene()
    bad = BadSetupScene()

    assert manager.switch_to(good) is True
    assert manager.current is good

    assert manager.switch_to(bad) is False
    assert manager.current is good


def test_switch_aborts_on_current_teardown_error() -> None:
    manager = SceneManager(types.SimpleNamespace())
    bad_current = BadOutScene()
    good_new = DummyScene()

    assert manager.switch_to(bad_current) is True
    assert manager.current is bad_current

    assert manager.switch_to(good_new) is False
    assert manager.current is bad_current
    assert good_new.calls == ["setup", "in", "out", "teardown"]


def test_switch_aborts_on_overlay_teardown_error() -> None:
    manager = SceneManager(types.SimpleNamespace())
    base = DummyScene()
    bad_overlay = BadOverlay()
    new_scene = DummyScene()

    assert manager.switch_to(base) is True
    assert manager.push_overlay(bad_overlay) is True

    assert manager.switch_to(new_scene) is False
    assert manager.current is base
    assert manager.overlays == [bad_overlay]
    assert new_scene.calls == ["setup", "in", "out", "teardown"]


def test_pop_overlay_failure_leaves_overlay() -> None:
    manager = SceneManager(types.SimpleNamespace())
    bad = BadOverlay()
    assert manager.push_overlay(bad) is True
    assert manager.pop_overlay() is False
    assert manager.overlays == [bad]


def test_overlays_teardown_in_reverse_order() -> None:
    manager = SceneManager(types.SimpleNamespace())
    order: list[str] = []

    class NamedOverlay(DummyScene):
        def __init__(self, name: str) -> None:
            super().__init__()
            self.name = name

        def transition_out(self) -> None:  # type: ignore[override]
            order.append(f"out-{self.name}")

        def teardown(self) -> None:  # type: ignore[override]
            order.append(f"teardown-{self.name}")

    first = NamedOverlay("first")
    second = NamedOverlay("second")

    assert manager.push_overlay(first) is True
    assert manager.push_overlay(second) is True
    assert manager.switch_to(DummyScene()) is True
    assert order == [
        "out-second",
        "teardown-second",
        "out-first",
        "teardown-first",
    ]

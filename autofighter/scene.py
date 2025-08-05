from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from direct.showbase.ShowBase import ShowBase
else:  # pragma: no cover - runtime avoids heavy import
    ShowBase = object


class Scene:
    def setup(self) -> None:
        """Initialize scene objects."""
        pass

    def teardown(self) -> None:
        """Clean up scene objects."""
        pass


class SceneManager:
    def __init__(self, base: ShowBase) -> None:
        self.base = base
        self.current: Scene | None = None
        self.overlays: list[Scene] = []

    def switch_to(self, scene: Scene | None) -> None:
        if self.current:
            self.current.teardown()
        for overlay in self.overlays:
            overlay.teardown()
        self.current = scene
        self.overlays = []
        if self.current:
            self.current.setup()

    def push_overlay(self, overlay: Scene) -> None:
        self.overlays.append(overlay)
        overlay.setup()

    def pop_overlay(self) -> None:
        if not self.overlays:
            return
        overlay = self.overlays.pop()
        overlay.teardown()

from __future__ import annotations

import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from direct.showbase.ShowBase import ShowBase
else:  # pragma: no cover - runtime avoids heavy import
    ShowBase = object

logger = logging.getLogger(__name__)


class Scene:
    def setup(self) -> None:
        """Initialize scene objects."""
        pass

    def transition_in(self) -> None:
        """Optional hook for entering animations or fades."""
        pass

    def transition_out(self) -> None:
        """Optional hook for exit animations or cleanup."""
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
            try:
                self.current.transition_out()
            except Exception:
                logger.exception("Error transitioning out scene %s", self.current)
            try:
                self.current.teardown()
            except Exception:
                logger.exception("Error tearing down scene %s", self.current)
        for overlay in self.overlays:
            try:
                overlay.transition_out()
            except Exception:
                logger.exception("Error transitioning out overlay %s", overlay)
            try:
                overlay.teardown()
            except Exception:
                logger.exception("Error tearing down overlay %s", overlay)
        self.current = None
        self.overlays = []
        if scene:
            try:
                scene.setup()
            except Exception:
                logger.exception("Error setting up scene %s", scene)
            else:
                try:
                    scene.transition_in()
                except Exception:
                    logger.exception("Error transitioning in scene %s", scene)
                self.current = scene

    def push_overlay(self, overlay: Scene) -> None:
        try:
            overlay.setup()
        except Exception:
            logger.exception("Error setting up overlay %s", overlay)
            return
        try:
            overlay.transition_in()
        except Exception:
            logger.exception("Error transitioning in overlay %s", overlay)
            try:
                overlay.teardown()
            except Exception:
                logger.exception("Error tearing down overlay %s", overlay)
            return
        self.overlays.append(overlay)

    def pop_overlay(self) -> None:
        if not self.overlays:
            return
        overlay = self.overlays.pop()
        try:
            overlay.transition_out()
        except Exception:
            logger.exception("Error transitioning out overlay %s", overlay)
        try:
            overlay.teardown()
        except Exception:
            logger.exception("Error tearing down overlay %s", overlay)

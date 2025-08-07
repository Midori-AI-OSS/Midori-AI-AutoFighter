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

    def switch_to(self, scene: Scene | None) -> bool:
        """Switch to ``scene`` and return ``True`` on success."""

        if scene is None:
            for overlay in reversed(self.overlays):
                try:
                    overlay.transition_out()
                except Exception:
                    logger.exception("Error transitioning out overlay %s", overlay)
                    return False
                try:
                    overlay.teardown()
                except Exception:
                    logger.exception("Error tearing down overlay %s", overlay)
                    return False
            self.overlays = []
            if self.current:
                try:
                    self.current.transition_out()
                except Exception:
                    logger.exception("Error transitioning out scene %s", self.current)
                    return False
                try:
                    self.current.teardown()
                except Exception:
                    logger.exception("Error tearing down scene %s", self.current)
                    return False
                self.current = None
            return True

        try:
            scene.setup()
        except Exception:
            logger.exception("Error setting up scene %s", scene)
            return False
        try:
            scene.transition_in()
        except Exception:
            logger.exception("Error transitioning in scene %s", scene)
            self._rollback(scene)
            return False

        for overlay in reversed(self.overlays):
            try:
                overlay.transition_out()
                overlay.teardown()
            except Exception:
                logger.exception("Error tearing down overlay %s", overlay)
                self._rollback(scene)
                return False
        if self.current:
            try:
                self.current.transition_out()
                self.current.teardown()
            except Exception:
                logger.exception("Error tearing down scene %s", self.current)
                self._rollback(scene)
                return False
        self.current = scene
        self.overlays = []
        return True

    def push_overlay(self, overlay: Scene) -> bool:
        try:
            overlay.setup()
            overlay.transition_in()
        except Exception:
            logger.exception("Error preparing overlay %s", overlay)
            self._rollback(overlay)
            return False
        self.overlays.append(overlay)
        return True

    def pop_overlay(self) -> bool:
        if not self.overlays:
            return True
        overlay = self.overlays[-1]
        try:
            overlay.transition_out()
            overlay.teardown()
        except Exception:
            logger.exception("Error removing overlay %s", overlay)
            return False
        self.overlays.pop()
        return True

    def _rollback(self, scene: Scene) -> None:
        try:
            scene.transition_out()
        except Exception:
            logger.exception("Error transitioning out scene %s during rollback", scene)
        try:
            scene.teardown()
        except Exception:
            logger.exception("Error tearing down scene %s during rollback", scene)

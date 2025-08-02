from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class HotPlugin(Protocol):
    """Protocol for healing-over-time plugins."""

    plugin_type: str
    id: str
    name: str

    def tick(self, target: Player, dt: int = 1) -> bool:
        """Apply healing to ``target`` and return ``True`` while active."""
        ...

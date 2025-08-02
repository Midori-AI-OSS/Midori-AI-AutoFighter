from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class PlayerPlugin(Protocol):
    """Protocol for player plugins."""

    plugin_type: str
    id: str
    name: str

    def build(self, **kwargs) -> "Player":
        """Construct and return a Player instance."""
        ...

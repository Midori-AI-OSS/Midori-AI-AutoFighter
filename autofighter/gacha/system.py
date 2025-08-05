"""Core gacha system exposing pity state."""

from __future__ import annotations

from dataclasses import dataclass

from .pity import Pity


@dataclass
class GachaSystem:
    """Gacha manager providing access to the pity tracker."""

    pity: Pity = Pity()

    def pull(self, featured: bool) -> None:
        """Record a pull outcome and update pity."""
        self.pity.record_pull(featured)

    def pity_count(self) -> int:
        """Return pulls since the last featured character."""
        return self.pity.pulls_without_featured

    def pity_chance(self) -> float:
        """Return current odds for the featured character."""
        return self.pity.chance()

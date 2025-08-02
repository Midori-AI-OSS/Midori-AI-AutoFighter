from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class WeaponPlugin(Protocol):
    """Protocol for weapon plugins."""

    plugin_type: str
    id: str
    name: str

    def attack(self, attacker: Player, target: Player) -> float:
        """Deal damage from ``attacker`` to ``target`` and return the amount."""
        ...

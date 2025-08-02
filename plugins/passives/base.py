from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - imported for type hints only
    from player import Player


class PassiveType:
    """Base type for all passives."""

    def __init__(self, name: str):
        self.name = name
        self.power: float = 1

    def activate(self, gamestate) -> None:  # noqa: D401
        """Applies the passive effect."""
        return gamestate

    def do_pre_turn(self):  # noqa: D401
        """Hook before a turn begins."""

    def heal_damage(self, input_healing: float):  # noqa: D401
        """Modify incoming healing."""

    def take_damage(self, input_damage: float):  # noqa: D401
        """Modify incoming damage."""

    def deal_damage(self, input_damage_mod: float):  # noqa: D401
        """Modify outgoing damage."""

    def damage_mitigation(self, damage_pre: float):  # noqa: D401
        """Adjust damage mitigation effects."""

    def regain_hp(self):  # noqa: D401
        """Adjust HP regain effects."""

    def damage_over_time(self):  # noqa: D401
        """Tick damage-over-time effects."""

    def heal_over_time(self):  # noqa: D401
        """Tick healing-over-time effects."""

    def crit_damage_mod(self, damage_pre: float):  # noqa: D401
        """Modify critical damage scaling."""


class PassivePlugin(PassiveType, ABC):
    """Base class for passive plugins."""

    plugin_type: str
    id: str
    name: str

    @abstractmethod
    def on_apply(self, player: "Player") -> None:  # noqa: D401
        """Grant the passive's effect to ``player``."""
        raise NotImplementedError

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from passives_folder.template_passive import PassiveType

if TYPE_CHECKING:
    from player import Player


class PassivePlugin(PassiveType, ABC):
    """Base class for passive plugins."""

    plugin_type: str
    id: str
    name: str

    @abstractmethod
    def on_apply(self, player: "Player") -> None:  # noqa: D401
        """Grant the passive's effect to ``player``."""
        raise NotImplementedError

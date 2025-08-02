from typing import Any, Dict, Optional

from damagetypes import Generic
from damagetypes import DamageType
from plugins.hots.base import HotPlugin
from plugins.plugin_loader import PluginLoader

class hot:
    """
    Represents a Healing Over Time (HOT) effect applied to a character or entity.

    Attributes:
        name (str): The name of the HOT effect (e.g., "Poison," "Burn").
        healing (int): The amount of healing dealt per turn by the HOT.
        turns (int): The number of turns the HOT effect lasts.  Must be greater than 0.
        healing_type (DamageType):  The type of healing the HOT inflicts (e.g., "fire", "poison", "bleed").
        source (Optional[str]):  Optional name or identifier of the entity that applied the HOT.  Helps track responsibility.
        metadata (Optional[Dict[str, Any]]):  Optional dictionary for storing extra information, like the spell or ability that caused the HOT.
        tick_interval (int): how many times to do the effect each turn, good if you want to do it fast and for less time.

    Raises:
        ValueError: If 'turns' is not a integer.
    """
    def __init__(self, name: str, healing: int, turns: int, healing_type: DamageType = Generic, source: Optional[str] = None, tick_interval: int = 1, metadata: Optional[Dict[str, Any]] = None) -> None:
        if not isinstance(turns, int):
            raise ValueError("Turns must be a integer.")

        self.name: str = name
        self.healing: int = healing
        self.turns: int = turns
        self.healing_type: DamageType = healing_type
        self.source: Optional[str] = source
        self.metadata: Optional[Dict[str, Any]] = metadata
        self.tick_interval: int = tick_interval

    def __repr__(self) -> str:
        return f"HOT(name='{self.name}', healing={self.healing}, turns={self.turns}, type={self.healing_type})"

    def tick(self) -> int:
        """
        Reduces the remaining duration of the HOT.

        Returns:
            The healing dealt this tick.  Returns 0 if the HOT has expired.
        """
        if self.turns > 0:
            self.turns -= 1
            return self.healing
        
        return 0

    def is_active(self) -> bool:
        """
        Checks if the HOT is still active (has remaining turns).

        Returns:
            True if the HOT is active, False otherwise.
        """
        return self.turns > 0


def get_hot(
    hot_id: str,
    *,
    plugin_dir: str = "plugins",
    **kwargs: Any,
) -> HotPlugin | hot:
    """Return a HOT plugin instance or fallback ``hot``."""

    loader = PluginLoader()
    loader.discover(plugin_dir)
    hot_cls = loader.get_plugins("hot").get(hot_id)
    if hot_cls is not None:
        return hot_cls(**kwargs)
    return hot(**kwargs)
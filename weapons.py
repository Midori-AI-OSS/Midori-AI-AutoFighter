from __future__ import annotations

from typing import Dict, Tuple, Type

from plugins.plugin_loader import PluginLoader
from plugins.weapons.base import WeaponPlugin

class WeaponType:
    """Represents a weapon type with its attributes and passive effect."""

    def __init__(self, name: str, damage: int, accuracy: float, critical_chance: float, game_str: str) -> None:
        """Initializes a WeaponType object.

        Args:
            name: The name of the weapon.
            damage: The base damage of the weapon.
            accuracy: The accuracy of the weapon (0.0 to 1.0).
            critical_chance: The critical hit chance (0.0 to 1.0).
            passive: A callable or an object with an 'activate' method representing the passive effect.
            game_str: A string representation of the weapon in the game.
        """
        self.name = name
        self.damage = damage
        self.accuracy = accuracy
        self.critical_chance = critical_chance
        self.game_obj = game_str
        self.position: Tuple[int, int] = (0, 0)  # type: ignore


DEFAULT_WEAPONS: Dict[str, WeaponType] = {
    "sword": WeaponType("Sword", 1, 1.0, 0.0, "Sword"),
}


def get_weapon(weapon_id: str) -> WeaponPlugin | WeaponType | None:
    """Return a weapon plugin instance or fallback ``WeaponType``."""

    loader = PluginLoader()
    loader.discover("plugins")
    weapon_cls: Type[WeaponPlugin] | None = loader.get_plugins("weapon").get(weapon_id)
    if weapon_cls is not None:
        return weapon_cls()
    return DEFAULT_WEAPONS.get(weapon_id)

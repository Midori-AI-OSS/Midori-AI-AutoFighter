"""Asset management utilities for Autofighter."""

from typing import Any

from .manager import AssetManager

ASSETS = AssetManager()


def get_asset(category: str, name: str) -> Any:
    """Return an asset by ``category`` and ``name``."""

    return ASSETS.load(category, name)


def get_model(name: str) -> Any:
    return ASSETS.get_model(name)


def get_texture(name: str) -> Any:
    return ASSETS.get_texture(name)


def get_audio(name: str) -> Any:
    return ASSETS.get_audio(name)


def get_player_photo(name: str) -> Any:
    return ASSETS.get_player_photo(name)


__all__ = [
    "AssetManager",
    "ASSETS",
    "get_asset",
    "get_model",
    "get_texture",
    "get_audio",
    "get_player_photo",
]

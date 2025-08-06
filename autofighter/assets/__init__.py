"""Asset management utilities for Autofighter."""

from typing import Any

from .manager import AssetManager

ASSETS = AssetManager()


def get_model(name: str) -> Any:
    return ASSETS.get_model(name)


def get_texture(name: str) -> Any:
    return ASSETS.get_texture(name)


def get_audio(name: str) -> Any:
    return ASSETS.get_audio(name)


__all__ = [
    "AssetManager",
    "ASSETS",
    "get_model",
    "get_texture",
    "get_audio",
]

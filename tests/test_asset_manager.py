from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from autofighter.assets import get_audio
from autofighter.assets import get_model
from autofighter.assets import get_texture
from autofighter.assets import AssetManager


def test_manifest_parsing_and_caching() -> None:
    manager = AssetManager(Path("assets.toml"))
    assert "cube" in manager.manifest["models"]

    first = manager.load("models", "cube")
    second = manager.load("models", "cube")
    assert first is second


def test_load_each_category() -> None:
    manager = AssetManager(Path("assets.toml"))
    tex1 = manager.load("textures", "white")
    tex2 = manager.load("textures", "white")
    aud1 = manager.load("audio", "boss_theme")
    aud2 = manager.load("audio", "boss_theme")
    assert tex1 is tex2 and tex1 is not None
    assert aud1 is aud2 and aud1 is not None

def test_hash_verification_failure() -> None:
    manager = AssetManager(Path("assets.toml"))
    manager.manifest["models"]["cube"]["sha256"] = "bad"
    with pytest.raises(ValueError):
        manager.load("models", "cube")


def test_asset_getters() -> None:
    manager = AssetManager(Path("assets.toml"))
    assert manager.get_model("cube") is manager.get_model("cube")
    assert manager.get_texture("white") is manager.get_texture("white")
    assert manager.get_audio("boss_theme") is manager.get_audio("boss_theme")


def test_module_level_helpers() -> None:
    assert get_model("cube") is get_model("cube")
    assert get_texture("white") is get_texture("white")
    assert get_audio("boss_theme") is get_audio("boss_theme")

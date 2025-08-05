from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from autofighter.assets import AssetManager


def test_manifest_parsing_and_caching() -> None:
    manager = AssetManager(Path("assets.toml"))
    assert "placeholder" in manager.manifest["models"]

    first = manager.load("models", "placeholder")
    second = manager.load("models", "placeholder")
    assert first is second

def test_hash_verification_failure() -> None:
    manager = AssetManager(Path("assets.toml"))
    manager.manifest["models"]["placeholder"]["sha256"] = "bad"
    with pytest.raises(ValueError):
        manager.load("models", "placeholder")

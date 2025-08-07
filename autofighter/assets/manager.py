from __future__ import annotations

import random
import hashlib
import tomllib

from typing import Any
from pathlib import Path

try:
    from panda3d.core import Loader
    from panda3d.core import TexturePool

    _PANDA_LOADER = Loader.get_global_ptr()
except Exception:  # pragma: no cover - Panda3D may be missing in tests
    _PANDA_LOADER = None
    TexturePool = None


class AssetManager:
    """Load and cache game assets defined in ``assets.toml``."""

    def __init__(self, manifest_path: Path | str = Path("assets.toml")) -> None:
        self.manifest_path = Path(manifest_path)
        with self.manifest_path.open("rb") as handle:
            self.manifest = tomllib.load(handle)
        self.cache: dict[str, dict[str, Any]] = {
            "models": {},
            "textures": {},
            "audio": {},
            "player_photos": {},
        }

    def _verify(self, file_path: Path, expected_hash: str) -> None:
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        if digest != expected_hash:
            raise ValueError(f"hash mismatch for {file_path}")

    def _load_file(self, category: str, file_path: Path) -> Any:
        if _PANDA_LOADER:
            os_path = file_path.as_posix()
            if category == "models":
                if hasattr(_PANDA_LOADER, "loadModel"):
                    return _PANDA_LOADER.loadModel(os_path)
                if hasattr(_PANDA_LOADER, "load_model"):
                    return _PANDA_LOADER.load_model(os_path)
            if category == "textures" and TexturePool:
                if hasattr(TexturePool, "loadTexture"):
                    return TexturePool.loadTexture(os_path)
                if hasattr(TexturePool, "load_texture"):
                    return TexturePool.load_texture(os_path)
            if category == "audio":
                if hasattr(_PANDA_LOADER, "loadSound"):
                    return _PANDA_LOADER.loadSound(os_path)
                if hasattr(_PANDA_LOADER, "load_sound"):
                    return _PANDA_LOADER.load_sound(os_path)
        return file_path.read_bytes()

    def load(self, category: str, name: str) -> Any:
        """Return an asset by ``category`` and ``name``.

        Assets are cached after the first load and verified against their
        ``sha256`` from the manifest.
        """

        cached = self.cache.get(category, {}).get(name)
        if cached is not None:
            return cached

        entry = self.manifest[category][name]
        file_path = Path(entry["path"])
        self._verify(file_path, entry["sha256"])
        asset = self._load_file(category, file_path)
        self.cache[category][name] = asset
        return asset

    def get_model(self, name: str) -> Any:
        """Return a model asset by ``name``."""

        return self.load("models", name)

    def get_texture(self, name: str) -> Any:
        """Return a texture asset by ``name``."""

        return self.load("textures", name)

    def get_audio(self, name: str) -> Any:
        """Return an audio asset by ``name``."""

        return self.load("audio", name)

    def get_player_photo(self, name: str) -> Any:
        """Return a player photo by ``name`` with fallback handling."""

        cached = self.cache["player_photos"].get(name)
        if cached is not None:
            return cached

        photos = self.manifest.get("player_photos", {})
        entry = photos.get(name)
        if entry is None:
            fallbacks = [v for k, v in photos.items() if k.startswith("fallback_")]
            if not fallbacks:
                raise KeyError(f"player photo '{name}' not found and no fallbacks defined")
            entry = random.choice(fallbacks)

        file_path = Path(entry["path"])
        self._verify(file_path, entry["sha256"])
        asset = self._load_file("textures", file_path)
        self.cache["player_photos"][name] = asset
        return asset

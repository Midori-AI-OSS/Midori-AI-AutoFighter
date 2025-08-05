from __future__ import annotations

import hashlib
import tomllib

from typing import Any
from pathlib import Path

try:
    from panda3d.core import Loader

    _PANDA_LOADER = Loader.get_global_ptr()
except Exception:  # pragma: no cover - Panda3D may be missing in tests
    _PANDA_LOADER = None


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
        }

    def _verify(self, file_path: Path, expected_hash: str) -> None:
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        if digest != expected_hash:
            raise ValueError(f"hash mismatch for {file_path}")

    def _load_file(self, category: str, file_path: Path) -> Any:
        if _PANDA_LOADER:
            if category == "models":
                return _PANDA_LOADER.load_model(file_path.as_posix())
            if category == "textures":
                return _PANDA_LOADER.load_texture(file_path.as_posix())
            if category == "audio":
                return _PANDA_LOADER.load_sound(file_path.as_posix())
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

from __future__ import annotations

from pathlib import Path

from plugins import PluginLoader


loader = PluginLoader()
loader.discover(str(Path(__file__).resolve().parent))
_plugins = loader.get_plugins("themedadj")

for cls in _plugins.values():
    globals()[cls.__name__] = cls

__all__ = sorted(cls.__name__ for cls in _plugins.values())


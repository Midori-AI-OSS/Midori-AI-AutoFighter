from __future__ import annotations

from typing import Any, Optional

from plugins.passives.base import PassivePlugin
from plugins.plugin_loader import PluginLoader


def get_passive(
    passive_id: str,
    *,
    plugin_dir: str = "plugins",
    **kwargs: Any,
) -> Optional[PassivePlugin]:
    """Return a passive plugin instance if available."""

    loader = PluginLoader()
    loader.discover(plugin_dir)
    passive_cls = loader.get_plugins("passive").get(passive_id)
    if passive_cls is not None:
        return passive_cls(**kwargs)
    return None

from pathlib import Path

from plugins import PluginLoader
from plugins.relics._base import RelicBase

from .party import Party

_loader: PluginLoader | None = None

def _registry() -> dict[str, type[RelicBase]]:
    global _loader
    if _loader is None:
        plugin_dir = Path(__file__).resolve().parents[1] / "plugins" / "relics"
        _loader = PluginLoader(required=["relic"])
        _loader.discover(str(plugin_dir))
    return _loader.get_plugins("relic")

def award_relic(party: Party, relic_id: str) -> RelicBase | None:
    relic_cls = _registry().get(relic_id)
    if relic_cls is None:
        return None
    party.relics.append(relic_id)
    return relic_cls()

def apply_relics(party: Party) -> None:
    registry = _registry()
    for rid in party.relics:
        relic_cls = registry.get(rid)
        if relic_cls:
            relic_cls().apply(party)

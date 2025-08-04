import importlib.util

from types import ModuleType
from pathlib import Path

from plugins.event_bus import EventBus


class PluginLoader:
    # never touch or load legacy code
    def __init__(self, bus: EventBus | None = None) -> None:
        self.bus = bus
        self._registry: dict[str, dict[str, type]] = {}

    def discover(self, root: str) -> None:
        base = Path(root)
        if not base.exists():
            return
        for path in base.rglob("*.py"):
            if path.name == "__init__.py":
                continue
            try:
                module = self._import_module(path)
            except Exception:
                continue
            self._register_module(module)

    def get_plugins(self, category: str) -> dict[str, type]:
        return self._registry.get(category, {})

    def _import_module(self, path: Path) -> ModuleType:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _register_module(self, module: ModuleType) -> None:
        for obj in module.__dict__.values():
            if isinstance(obj, type) and getattr(obj, "plugin_type", None):
                category = obj.plugin_type
                plugin_id = getattr(obj, "id", obj.__name__)
                self._registry.setdefault(category, {})[plugin_id] = obj
                if self.bus is not None:
                    setattr(obj, "bus", self.bus)

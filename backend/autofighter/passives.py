from __future__ import annotations

from collections import Counter

from plugins import passives as passive_plugins


class PassiveRegistry:
    def __init__(self) -> None:
        self._registry = {
            getattr(passive_plugins, name).id: getattr(passive_plugins, name)
            for name in getattr(passive_plugins, "__all__", [])
        }

    def trigger(self, event: str, target) -> None:
        counts = Counter(target.passives)
        for pid, count in counts.items():
            cls = self._registry.get(pid)
            if cls is None or getattr(cls, "trigger", None) != event:
                continue
            stacks = min(count, getattr(cls, "max_stacks", count))
            for _ in range(stacks):
                cls().apply(target)

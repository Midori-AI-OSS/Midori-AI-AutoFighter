import logging

from collections import defaultdict
from typing import Any
from typing import Callable

try:
    from rich.logging import RichHandler
except Exception:  # pragma: no cover - fallback when Rich is missing
    RichHandler = logging.StreamHandler


class _Bus:
    def __init__(self) -> None:
        self._subs: dict[str, list[tuple[object, Callable[..., Any]]]] = defaultdict(list)

    def accept(self, event: str, obj, func: Callable[..., Any]) -> None:
        self._subs[event].append((obj, func))

    def ignore(self, event: str, obj) -> None:
        self._subs[event] = [
            pair for pair in self._subs.get(event, []) if pair[0] is not obj
        ]

    def send(self, event: str, args) -> None:
        for _, func in list(self._subs.get(event, [])):
            func(*args)


bus = _Bus()

log = logging.getLogger(__name__)
if not log.handlers:
    log.addHandler(RichHandler())


class EventBus:
    def subscribe(self, event: str, callback: Callable[..., Any]) -> None:
        def wrapper(*args: Any) -> None:
            try:
                callback(*args)
            except Exception:
                log.exception("Error in '%s' subscriber %s", event, callback)

        bus.accept(event, callback, wrapper)

    def unsubscribe(self, event: str, callback: Callable[..., Any]) -> None:
        bus.ignore(event, callback)

    def emit(self, event: str, *args: Any) -> None:
        bus.send(event, args)

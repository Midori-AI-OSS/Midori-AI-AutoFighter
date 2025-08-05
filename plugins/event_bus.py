import logging

from typing import Any
from typing import Callable

from rich.logging import RichHandler
from direct.showbase.MessengerGlobal import messenger


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

        messenger.accept(event, callback, wrapper)

    def unsubscribe(self, event: str, callback: Callable[..., Any]) -> None:
        messenger.ignore(event, callback)

    def emit(self, event: str, *args: Any) -> None:
        messenger.send(event, args)

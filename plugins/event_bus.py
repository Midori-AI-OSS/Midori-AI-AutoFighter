from typing import Any
from typing import Callable

from direct.showbase.MessengerGlobal import messenger


class EventBus:
    def subscribe(self, event: str, callback: Callable[..., Any]) -> None:
        messenger.accept(event, callback, callback)

    def unsubscribe(self, event: str, callback: Callable[..., Any]) -> None:
        messenger.ignore(event, callback)

    def emit(self, event: str, *args: Any) -> None:
        messenger.send(event, args)

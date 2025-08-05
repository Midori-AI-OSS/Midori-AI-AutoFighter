# Event Bus Wrapper

Provides a thin layer over Panda3D's `messenger` so plugins can communicate without importing engine modules.

## Usage
- `subscribe(event: str, callback: Callable)` – register a function to run when an event is emitted.
- `unsubscribe(event: str, callback: Callable)` – stop receiving a previously subscribed event.
- `emit(event: str, *args)` – broadcast an event with optional arguments.

Subscriber errors are caught and logged so one misbehaving plugin does not crash others.

## Events
No global events are defined yet. Plugins may define and document their own event names.

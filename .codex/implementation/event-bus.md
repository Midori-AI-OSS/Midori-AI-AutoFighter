# Event Bus Wrapper

Provides a simple publish/subscribe bus so plugins can communicate without engine-specific dependencies.

## Usage
- `subscribe(event: str, callback: Callable)` – register a function to run when an event is emitted.
- `unsubscribe(event: str, callback: Callable)` – stop receiving a previously subscribed event.
- `emit(event: str, *args)` – broadcast an event with optional arguments.

Subscriber errors are caught and logged so one misbehaving plugin does not crash others.

## Events
No global events are defined yet. Plugins may define and document their own event names.

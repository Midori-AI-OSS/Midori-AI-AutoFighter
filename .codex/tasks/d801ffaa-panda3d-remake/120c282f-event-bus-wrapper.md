# Event Bus Wrapper

## Summary
Expose a decoupled messaging interface so plugins can emit and subscribe without direct Panda3D imports.

## Tasks
- [x] Wrap Panda3D's `messenger` with subscribe and emit helpers.
- [x] Prevent plugin crashes from propagating through the bus.
- [x] Document available events and usage.
- [x] Document this feature in `.codex/implementation`.
- [x] Add unit tests covering success and failure cases.

## Context
An event bus lets plugins communicate while remaining isolated from the engine.

## Testing
- [x] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.

status: ready for review

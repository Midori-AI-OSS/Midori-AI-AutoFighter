# Main Loop and Window Handling

## Summary
Implement the Panda3D application loop, scene management, and input hooks.

## Tasks
- [ ] Expand `main.py` with a `ShowBase` subclass to manage the app lifecycle.
- [ ] Route events through Panda3D's `messenger` and schedule updates with `taskMgr`.
- [ ] Add a lightweight scene manager for swapping menus, gameplay states, and overlays.
- [ ] Handle window close events and keyboard input for quitting the game.
- [ ] Set the window title to the game's name.

## Context
A robust main loop with scene switching is required before integrating menus, maps, or combat systems.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.

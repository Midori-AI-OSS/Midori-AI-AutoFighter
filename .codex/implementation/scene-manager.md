# Scene Manager

Coordinates swapping scenes and managing overlay stacks.

## Lifecycle
- `switch_to(scene)` – transition out the current scene and overlays, tear them down, then set up and transition into the new scene.
- `push_overlay(overlay)` – set up and transition into an overlay while keeping the current scene active.
- `pop_overlay()` – transition out and tear down the most recently pushed overlay.

Scenes provide optional hooks:
- `setup()` and `teardown()` for allocating and releasing resources.
- `transition_in()` and `transition_out()` for entrance and exit animations.

Errors in hooks are caught and logged so a faulty scene does not halt the application.

# Scene Manager

Coordinates swapping scenes and managing overlay stacks.

## Lifecycle
- `switch_to(scene)` – set up and transition into the new scene before tearing down overlays and the current scene. Overlays are dismantled in LIFO order. Returns `True` on success and rolls back the new scene while leaving the existing state intact if any hook fails.
- `push_overlay(overlay)` – set up and transition into an overlay while keeping the current scene active. Returns `True` on success and rolls back the overlay on failure.
- `pop_overlay()` – transition out and tear down the most recently pushed overlay. Returns `True` on success and `False` if teardown fails; the overlay remains on the stack when removal fails.

Scenes provide optional hooks:
- `setup()` and `teardown()` for allocating and releasing resources.
- `transition_in()` and `transition_out()` for entrance and exit animations.

Errors in hooks are caught, logged, and rolled back so a faulty scene does not halt the application or leave partial state.

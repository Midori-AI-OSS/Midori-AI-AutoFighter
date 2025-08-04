# Panda3D Plugin Loader

## Summary
Create a plugin-loading system compatible with the Panda3D remake.

## Tasks
- [ ] Implement a loader that discovers Python modules under `plugins/` and registers them with the game.
- [ ] Provide hooks for player, weapon, foe, passive, DoT, HoT, and room plugins.
- [ ] Expose a mod interface and avoid importing legacy Pygame code.
- [ ] Wrap Panda3D's `messenger` with an event bus so plugins can subscribe and emit without engine imports.
- [ ] Document the plugin API and how to add new plugins.

## Context
A flexible plugin loader keeps the game extensible for new content.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.

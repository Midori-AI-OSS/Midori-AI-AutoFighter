# Panda3D Plugin Loader

## Summary
Create a plugin-loading system compatible with the Panda3D remake.

## Tasks
- [x] Implement a loader that discovers Python modules under `plugins/` and registers them with the game.
- [x] Provide hooks for player, weapon, foe, passive, DoT, HoT, and room plugins.
- [x] Expose a mod interface and avoid importing legacy Pygame code.
- [x] Wrap Panda3D's `messenger` with an event bus so plugins can subscribe and emit without engine imports.
- [x] Document the plugin API and how to add new plugins.

## Context
A flexible plugin loader keeps the game extensible for new content.

## Testing
- [x] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.

status: failed - discovery registers classes but several plugin categories (foes, passives, rooms) remain unverified; poison DoT missing and tests report unregistered plugins

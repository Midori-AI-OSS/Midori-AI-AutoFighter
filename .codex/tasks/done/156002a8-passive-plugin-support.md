# Passive Plugin Support

## Summary
Enable passive effects to be implemented as plugins and automatically loaded at boot, replacing the hard-coded definitions in `passives_folder` and related files.

## Tasks
- [x] Add `plugins/passives/base.py` defining a `PassivePlugin` protocol derived from `PassiveType` with hooks such as `on_apply`, `on_turn_start`, and damage callbacks.
- [x] Extend `plugins/plugin_loader.py` to scan `plugins/passives/` and register each implementation under the `passive` category.
- [x] Refactor `foe_passive_builder.py` and any direct passive imports to query the registry for available passives.
- [x] Relocate `passives_folder/bleeding_blow.py` to `plugins/passives/bleeding_blow.py` and adapt it to the new interface.

## Context
Passives are currently stored in a dedicated folder but not dynamically loaded. Using the plugin system will allow new passive effects without changing core game code.

## Testing
- [x] Add tests in `tests/test_passive_plugins.py` asserting that runtime-discovered passives trigger their hooks and alter game state.
- [x] Run the game with the `plugins/passives/` directory removed to confirm startup continues without available passives.

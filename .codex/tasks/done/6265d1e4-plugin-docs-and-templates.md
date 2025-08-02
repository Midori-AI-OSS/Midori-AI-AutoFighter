# Plugin Documentation and Examples

## Summary
Document the plugin system and provide developers with templates for creating new player, passive, dot, hot, and weapon plugins.

## Tasks
- [x] Add a guide at `.codex/instructions/plugin-system.md` detailing directory layout, required interfaces, and how the plugin loader discovers modules for player, passive, dot, hot, and weapon categories.
- [x] Create template files `plugins/templates/player_plugin.py`, `plugins/templates/passive_plugin.py`, `plugins/templates/dot_plugin.py`, `plugins/templates/hot_plugin.py`, and `plugins/templates/weapon_plugin.py` with docstrings and TODO markers for mandatory methods.
- [x] Update `README.md` to mention the `plugins/` folder, how to drop in new plugin modules for all categories, and any configuration flags needed to enable them.
- [x] Insert inline comments in `plugins/players/warrior.py`, `plugins/passives/bleeding_blow.py`, `plugins/dots/poison.py`, `plugins/hots/regeneration.py`, and `plugins/weapons/sword.py` describing expected fields and lifecycle hooks.

## Context
Clear documentation and templates will make it easier for contributors to add new players, passives, dots, hots, and weapons via the plugin system.

## Testing
- [x] Run `uv run python -m py_compile plugins/templates/*.py` to confirm template syntax validity.
- [x] Import the example templates via `plugins.plugin_loader` in a Python shell to ensure the loader can locate them.

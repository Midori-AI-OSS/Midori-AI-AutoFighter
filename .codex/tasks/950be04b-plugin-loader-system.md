# Plugin Loader Framework

## Summary
Create a generic plugin loader that discovers and imports plugin modules from a designated `plugins/` directory on game start.

## Tasks
- [x] Create `plugins/plugin_loader.py` containing a `PluginLoader` class with a `discover(plugin_dir: str)` method.
- [x] Configure the loader to scan a `plugins/` directory (default at repository root) using `importlib` to import each module dynamically.
- [x] Build an internal registry mapping plugin categories (e.g., `player`, `passive`, `dot`, `hot`, `weapon`) to discovered classes so game systems can query available implementations.
- [x] Implement error handling that catches `ImportError` and attribute errors, logs a clear message via the `logging` module, and continues loading remaining plugins.
- [x] Expose a `get_plugins(plugin_type: str) -> dict[str, type]` helper to retrieve classes for a given category.

## Context
Currently players and passives are hard coded across large files such as `player.py` and `buldfoepassives.py`. A generic loader is needed to support dynamic additions without modifying core code.

## Testing
- [x] Add tests in `tests/test_plugin_loader.py` asserting that valid modules are registered and malformed ones are skipped.
- [x] Run the game with an empty `plugins/` directory to ensure startup succeeds without plugins.

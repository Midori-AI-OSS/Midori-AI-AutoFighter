# DOT Plugin Support

## Summary
Enable damage-over-time effects to be implemented as plugins and loaded on boot rather than being hard coded in `damage_over_time.py`.

## Tasks
- [ ] Add `plugins/dots/base.py` defining a `DotPlugin` protocol with attributes like `id`, `name`, and a `build(**kwargs) -> dot` factory.
- [ ] Extend `plugins/plugin_loader.py` to scan `plugins/dots/` and register each implementation under the `dot` category.
- [ ] Refactor `damage_over_time.py` to request DOT implementations from the plugin registry and fall back to the existing `dot` class when no plugin matches.
- [ ] Move an existing DOT (e.g., poison) into `plugins/dots/poison.py` conforming to the new interface.

## Context
DOT effects are currently defined in `damage_over_time.py`, forcing edits for every new status effect. A plugin system lets contributors add new DOTs without modifying core code.

## Testing
- [ ] Add tests in `tests/test_dot_plugins.py` asserting that `plugins/dots/poison.py` registers and instances can be constructed.
- [ ] Run the game with `plugins/dots/` removed to ensure DOT loading gracefully falls back to legacy behavior.


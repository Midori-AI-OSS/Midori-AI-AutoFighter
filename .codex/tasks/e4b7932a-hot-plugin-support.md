# HOT Plugin Support

## Summary
Enable healing-over-time effects to be implemented as plugins and loaded on boot rather than hard coded in `healing_over_time.py`.

## Tasks
- [ ] Add `plugins/hots/base.py` defining a `HotPlugin` protocol with attributes like `id`, `name`, and a `build(**kwargs) -> hot` factory.
- [ ] Extend `plugins/plugin_loader.py` to scan `plugins/hots/` and register each implementation under the `hot` category.
- [ ] Refactor `healing_over_time.py` to request HOT implementations from the plugin registry and fall back to the existing `hot` class when no plugin matches.
- [ ] Move an existing HOT (e.g., regeneration) into `plugins/hots/regeneration.py` conforming to the new interface.

## Context
Healing over time effects are currently defined in `healing_over_time.py`. Turning them into plugins allows new effects without touching core files.

## Testing
- [ ] Add tests in `tests/test_hot_plugins.py` asserting that `plugins/hots/regeneration.py` registers and instances can be constructed.
- [ ] Run the game with `plugins/hots/` removed to confirm HOT loading falls back to legacy behavior.


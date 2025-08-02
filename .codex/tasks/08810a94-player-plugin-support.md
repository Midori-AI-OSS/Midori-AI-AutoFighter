# Player Plugin Support

## Summary
Refactor player creation so new player classes can be loaded as plugins instead of being embedded directly in `player.py` or `buldfoepassives.py`.

## Tasks
- [ ] Create `plugins/players/base.py` defining a `PlayerPlugin` protocol with required fields such as `id`, `name`, and `build(**kwargs) -> Player`.
- [ ] Extend `plugins/plugin_loader.py` to scan `plugins/players/` and register each `PlayerPlugin` under the `player` category.
- [ ] Refactor `player.py` and `buldfoepassives.py` to construct player instances by querying the plugin registry instead of using hard-coded classes.
- [ ] Move an existing player (e.g., the default warrior) into `plugins/players/warrior.py` as an example plugin.
- [ ] Provide a fallback path so legacy player definitions still load if no matching plugin is found.

## Context
Player behaviors and stats are presently derived from hard-coded logic, making it difficult to extend. A plugin-based approach will simplify adding new player types.

## Testing
- [ ] Add tests in `tests/test_player_plugins.py` confirming the example plugin registers and `Player` instances build successfully.
- [ ] Start a demo game using only legacy players and then with the plugin-enabled path to ensure both modes work.

# Weapon Plugin Support

## Summary
Allow weapons to be defined as plugins and loaded at runtime instead of being embedded directly in `weapons.py`.

## Tasks
- [x] Add `plugins/weapons/base.py` defining a `WeaponPlugin` protocol derived from `WeaponType` with required fields like `id`, `name`, and a `build(**kwargs) -> WeaponType` factory.
- [x] Extend `plugins/plugin_loader.py` to scan `plugins/weapons/` and register each implementation under the `weapon` category.
- [x] Refactor `weapons.py` to obtain weapon definitions from the plugin registry, preserving a fallback to the current `WeaponType` instances if no plugin exists.
- [x] Move an existing weapon (e.g., the default sword) into `plugins/weapons/sword.py` as an example plugin.

## Context
Weapons are currently defined in a single module, making it difficult to introduce new weapon types. A plugin-based approach simplifies extension.

## Testing
- [x] Add tests in `tests/test_weapon_plugins.py` verifying that `plugins/weapons/sword.py` registers and builds a `WeaponType` instance.
- [x] Run the game with `plugins/weapons/` absent to confirm legacy weapons still initialize.


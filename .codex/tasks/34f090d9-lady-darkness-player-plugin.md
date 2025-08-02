# Lady Darkness Player Plugin

## Summary
Create a plugin-based implementation for the Lady Darkness player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Lady Darkness` player plugin in `plugins/players/lady_darkness.py`.
- [ ] Move Lady Darkness-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Lady Darkness's player and passive work via `create_player`.

## Context
Lady Darkness's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

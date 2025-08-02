# Lady Of Fire Player Plugin

## Summary
Create a plugin-based implementation for the Lady Of Fire player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Lady Of Fire` player plugin in `plugins/players/lady_of_fire.py`.
- [ ] Move Lady Of Fire-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Lady Of Fire's player and passive work via `create_player`.

## Context
Lady Of Fire's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

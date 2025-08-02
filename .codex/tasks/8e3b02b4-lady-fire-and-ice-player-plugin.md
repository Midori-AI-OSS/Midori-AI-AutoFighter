# Lady Fire And Ice Player Plugin

## Summary
Create a plugin-based implementation for the Lady Fire And Ice player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Lady Fire And Ice` player plugin in `plugins/players/lady_fire_and_ice.py`.
- [ ] Move Lady Fire And Ice-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Lady Fire And Ice's player and passive work via `create_player`.

## Context
Lady Fire And Ice's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

# Lady Light Player Plugin

## Summary
Create a plugin-based implementation for the Lady Light player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Lady Light` player plugin in `plugins/players/lady_light.py`.
- [ ] Move Lady Light-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Lady Light's player and passive work via `create_player`.

## Context
Lady Light's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

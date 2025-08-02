# Kboshi Player Plugin

## Summary
Create a plugin-based implementation for the Kboshi player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Kboshi` player plugin in `plugins/players/kboshi.py`.
- [ ] Move Kboshi-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Kboshi's player and passive work via `create_player`.

## Context
Kboshi's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

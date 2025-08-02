# Mimic Player Plugin

## Summary
Create a plugin-based implementation for the Mimic player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Mimic` player plugin in `plugins/players/mimic.py`.
- [ ] Move Mimic-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Mimic's player and passive work via `create_player`.

## Context
Mimic's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

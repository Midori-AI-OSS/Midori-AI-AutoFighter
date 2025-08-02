# Carly Player Plugin

## Summary
Create a plugin-based implementation for the Carly player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Carly` player plugin in `plugins/players/carly.py`.
- [x] Move Carly-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Carly's player and passive work via `create_player`.

## Context
Carly's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

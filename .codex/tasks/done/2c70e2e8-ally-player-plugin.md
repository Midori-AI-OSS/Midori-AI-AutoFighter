# Ally Player Plugin

## Summary
Create a plugin-based implementation for the Ally player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Ally` player plugin in `plugins/players/ally.py`.
- [x] Move Ally-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Ally's player and passive work via `create_player`.

## Context
Ally's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

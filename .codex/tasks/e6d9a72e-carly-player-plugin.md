# Carly Player Plugin

## Summary
Create a plugin-based implementation for the Carly player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Carly` player plugin in `plugins/players/carly.py`.
- [ ] Move Carly-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Carly's player and passive work via `create_player`.

## Context
Carly's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

# Mimic Player Plugin

## Summary
Create a plugin-based implementation for the Mimic player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Mimic` player plugin in `plugins/players/mimic.py`.
- [ ] Move Mimic-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Mimic's player and passive work via `create_player`.

## Context
Mimic's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

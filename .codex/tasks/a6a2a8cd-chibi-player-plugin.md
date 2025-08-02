# Chibi Player Plugin

## Summary
Create a plugin-based implementation for the Chibi player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Chibi` player plugin in `plugins/players/chibi.py`.
- [ ] Move Chibi-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Chibi's player and passive work via `create_player`.

## Context
Chibi's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

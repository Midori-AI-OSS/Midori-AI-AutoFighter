# Hilander Player Plugin

## Summary
Create a plugin-based implementation for the Hilander player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Hilander` player plugin in `plugins/players/hilander.py`.
- [ ] Move Hilander-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Hilander's player and passive work via `create_player`.

## Context
Hilander's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

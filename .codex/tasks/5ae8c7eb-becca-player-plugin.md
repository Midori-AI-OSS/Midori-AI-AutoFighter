# Becca Player Plugin

## Summary
Create a plugin-based implementation for the Becca player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Becca` player plugin in `plugins/players/becca.py`.
- [ ] Move Becca-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Becca's player and passive work via `create_player`.

## Context
Becca's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

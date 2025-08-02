# Bubbles Player Plugin

## Summary
Create a plugin-based implementation for the Bubbles player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Bubbles` player plugin in `plugins/players/bubbles.py`.
- [ ] Move Bubbles-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Bubbles's player and passive work via `create_player`.

## Context
Bubbles's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

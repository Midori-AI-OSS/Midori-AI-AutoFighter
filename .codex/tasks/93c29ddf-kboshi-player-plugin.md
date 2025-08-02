# Kboshi Player Plugin

## Summary
Create a plugin-based implementation for the Kboshi player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Kboshi` player plugin in `plugins/players/kboshi.py`.
- [ ] Move Kboshi-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Kboshi's player and passive work via `create_player`.

## Context
Kboshi's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

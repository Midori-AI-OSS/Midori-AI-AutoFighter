# Mezzy Player Plugin

## Summary
Create a plugin-based implementation for the Mezzy player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Mezzy` player plugin in `plugins/players/mezzy.py`.
- [ ] Move Mezzy-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Mezzy's player and passive work via `create_player`.

## Context
Mezzy's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

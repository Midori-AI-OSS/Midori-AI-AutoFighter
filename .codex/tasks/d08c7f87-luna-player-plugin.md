# Luna Player Plugin

## Summary
Create a plugin-based implementation for the Luna player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Luna` player plugin in `plugins/players/luna.py`.
- [ ] Move Luna-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Luna's player and passive work via `create_player`.

## Context
Luna's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

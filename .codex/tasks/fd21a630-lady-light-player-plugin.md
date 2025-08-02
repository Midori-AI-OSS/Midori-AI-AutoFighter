# Lady Light Player Plugin

## Summary
Create a plugin-based implementation for the Lady Light player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Lady Light` player plugin in `plugins/players/lady-light.py`.
- [ ] Move Lady Light-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Lady Light's player and passive work via `create_player`.

## Context
Lady Light's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

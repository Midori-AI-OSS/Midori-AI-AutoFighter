# Lady Of Fire Player Plugin

## Summary
Create a plugin-based implementation for the Lady Of Fire player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Lady Of Fire` player plugin in `plugins/players/lady-of-fire.py`.
- [ ] Move Lady Of Fire-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Lady Of Fire's player and passive work via `create_player`.

## Context
Lady Of Fire's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

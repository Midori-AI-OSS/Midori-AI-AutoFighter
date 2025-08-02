# Lady Fire And Ice Player Plugin

## Summary
Create a plugin-based implementation for the Lady Fire And Ice player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Lady Fire And Ice` player plugin in `plugins/players/lady-fire-and-ice.py`.
- [ ] Move Lady Fire And Ice-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Lady Fire And Ice's player and passive work via `create_player`.

## Context
Lady Fire And Ice's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

# Lady Echo Player Plugin

## Summary
Create a plugin-based implementation for the Lady Echo player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Lady Echo` player plugin in `plugins/players/lady-echo.py`.
- [ ] Move Lady Echo-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Lady Echo's player and passive work via `create_player`.

## Context
Lady Echo's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

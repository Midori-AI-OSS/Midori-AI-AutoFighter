# Lady Echo Player Plugin

## Summary
Create a plugin-based implementation for the Lady Echo player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Lady Echo` player plugin in `plugins/players/lady_echo.py`.
- [ ] Move Lady Echo-specific passive effects from `damagestate.py` into a dedicated plugin under `plugins/passives/`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Lady Echo's player and passive work via `create_player`.

## Context
Lady Echo's stat modifiers are currently hard-coded in `damagestate.py`, and foe-only bonuses remain in `foe_passive_builder.py`.

## Testing
- [x] Run `uv run pytest`.

# Ally Player Plugin

## Summary
Create a plugin-based implementation for the Ally player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Ally` player plugin in `plugins/players/ally.py`.
- [ ] Move Ally-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Ally's player and passive work via `create_player`.

## Context
Ally's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

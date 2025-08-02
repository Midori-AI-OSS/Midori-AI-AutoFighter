# Graygray Player Plugin

## Summary
Create a plugin-based implementation for the Graygray player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Graygray` player plugin in `plugins/players/graygray.py`.
- [ ] Move Graygray-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Graygray's player and passive work via `create_player`.

## Context
Graygray's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

# Lady Darkness Player Plugin

## Summary
Create a plugin-based implementation for the Lady Darkness player and migrate its unique passive bonuses.

## Tasks
- [ ] Implement `Lady Darkness` player plugin in `plugins/players/lady-darkness.py`.
- [ ] Move Lady Darkness-specific passive effects from `foe_passive_builder.py` and `damagestate.py` into a dedicated plugin under `plugins/passives/`.
- [ ] Add tests verifying Lady Darkness's player and passive work via `create_player`.

## Context
Lady Darkness's stat modifiers are currently hard-coded in `foe_passive_builder.py` and `damagestate.py`.

## Testing
- [ ] Run `uv run pytest`.

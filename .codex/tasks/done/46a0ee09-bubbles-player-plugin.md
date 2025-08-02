# Bubbles Player Plugin

## Summary
Create a plugin-based implementation for the Bubbles player and migrate its unique passive bonuses.

## Tasks
- [x] Implement `Bubbles` player plugin in `plugins/players/bubbles.py`.
- [x] Implement Bubbles-specific passive in `plugins/passives/bubbles_passive.py`, leaving foe-only bonuses in `foe_passive_builder.py`.
- [x] Add tests verifying Bubbles's player and passive work via `create_player`.

## Context
Bubbles currently has foe-only item enhancements in `foe_passive_builder.py`. A dedicated player passive ensures players do not rely on foe logic.

## Testing
- [x] Run `uv run pytest`.

# Bleeding Blow Player Modification

## Summary
Add bleed chance support to player characters and update the Bleeding Blow passive plugin accordingly.

## Tasks
- [x] Extend `player.py` with a bleed chance attribute used by passives.
- [x] Implement bleed application logic in `plugins/passives/bleeding_blow.py`.
- [x] Provide an automated test verifying bleed chance modifies damage over time.

## Context
`plugins/passives/bleeding_blow.py` currently notes a TODO to modify the player for bleed mechanics.

## Testing
- [x] Run `uv run pytest` after implementing bleed logic and tests.

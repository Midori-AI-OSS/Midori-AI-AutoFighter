# Remove Warrior character completely

## Summary
Eliminate the erroneous `Warrior` player from the codebase, tests, and documentation.

## Details
- Delete `plugins/players/warrior.py` and any associated assets.
- Remove Warrior references from `tests/test_player_plugins.py` so the test suite no longer expects this plugin.
- Strip all mentions of Warrior from `README.md`, documentation files, and historical tasks if necessary.
- Verify the game launches and the test suite passes after removal.

## Notes
- Follow up on review comment noting Warrior was added by mistake.

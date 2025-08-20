# Preserve player editor stats between battles

## Context
- Allocations made in the Player Editor apply in the first fight but reset afterward.
- `load_party` in `backend/app.py` expects a `player` snapshot in the saved party to reapply custom stats via `_apply_player_stats`.
- `save_party` omits this snapshot, so subsequent loads rebuild the player with default stats.

## Task
1. Extend `save_party` in `backend/app.py` to include a `player` entry containing the player's current `damage_type` and `stats` (HP, attack, defense, etc.).
2. Confirm `load_party` continues to read this snapshot and apply `_apply_player_stats` when constructing the party.
3. Add a backend test ensuring stats edited via `/player/editor` persist across multiple battles without reverting.
4. Document the save data change in appropriate backend docs.
5. Run `uv run pytest` and `bun test` after implementing.

## Acceptance Criteria
- Player stat allocations remain intact for the entire run.
- New test verifies persistence across battles.
- `uv run pytest` and `bun test` executed.

Status: Need Review

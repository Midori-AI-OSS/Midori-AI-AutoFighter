# Fix enrage background animation

## Context
- Battle docs state the background should pulse red/blue when foes enter **Enrage** after the turn threshold (`.codex/instructions/battle-room.md`).
- In practice, the background never changes because `frontend/src/lib/BattleView.svelte` does not update its `enrage` state from battle snapshots.
- `rooms.py` includes `enrage` data in the snapshot payload, but the frontend ignores it, leaving `.battle-field.enraged` inactive.

## Task
1. In `fetchSnapshot()` inside `frontend/src/lib/BattleView.svelte`, assign `enrage` when the snapshot contains an `enrage` field and it differs from the current value.
2. Ensure `rooms.py` continues to expose `enrage` with `active` and `stacks` so the frontend can react.
3. Verify that when `enrage.active` becomes true, the `.battle-field` element gains the `enraged` class and the red/blue cycling animation plays.
4. Add a frontend regression test that simulates an enrage snapshot and confirms the class toggles.
5. Run `bun test` and `uv run pytest` after making changes.

## Acceptance Criteria
- Background animation activates once foes become enraged and stops when combat ends.
- New test covers enrage background behavior.
- `bun test` and `uv run pytest` executed.

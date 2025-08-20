# Fix Rest Room exit flow

## Context
- After winning a battle, entering a Rest Room leaves the player stuck; the "Leave" button emits an event but the next room never loads.
- `frontend/src/routes/+page.svelte` clears `nextRoom` when entering the Rest Room because `RestRoom.resolve` does not return a `next_room` property.
- `handleRestLeave` calls `advanceRoom` without capturing its response, so `nextRoom` stays empty and `enterRoom()` returns early.

## Task
1. Update `handleRestLeave` in `frontend/src/routes/+page.svelte` to store the `next_room` value returned by `advanceRoom` and assign it to `nextRoom` before calling `enterRoom()`.
2. Confirm that the Shop leave flow handles `next_room` similarly; adjust `handleShopLeave` if needed so both non-battle rooms can be exited.
3. Verify that clicking **Leave** in a Rest Room after a battle advances to the next map node.
4. Run `bun test` and `uv run pytest` to ensure existing tests pass (tests currently failing should be addressed separately).

## Acceptance Criteria
- Leaving a Rest Room after a battle loads the subsequent room without requiring a manual page refresh.
- Shop leave flow remains functional.
- All frontend tests pass (`bun test`).
- Backend test suite (`uv run pytest`) is executed with best effort.

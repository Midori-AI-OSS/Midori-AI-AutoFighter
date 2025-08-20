# Retain party picker selections and persist to backend

## Context
- Closing and reopening the Party Picker resets the selection to only the player.
- In `frontend/src/lib/PartyPicker.svelte`, `onMount` unconditionally assigns `selected = [player.id]`, discarding prior choices passed from the parent.
- The Party Picker never syncs selections to the backend, so runs forget party composition and no ownership check occurs.

## Task
1. Modify `onMount` in `PartyPicker.svelte` so it only defaults to the player when the incoming `selected` array is empty.
2. When the party confirmation button is used, send the selected IDs to the backend so the active run saves the full party.
3. Extend backend party save/load logic to return the stored party to the frontend on load and reject characters the player does not own.
4. Ensure existing selections from `GameViewport` persist when the component remounts and after a page refresh using data from the backend.
5. Add a frontend test that selects additional characters, closes and reopens the picker, refreshes the page, and asserts the selection is preserved.
6. Add a backend test that saves a party, reloads it, and fails when unowned characters are provided.
7. Run `bun test` and `uv run pytest` after changes.

## Acceptance Criteria
- Party choices survive closing and reopening the Party Picker and reloading the page.
- Backend stores and restores the party while refusing unowned characters.
- New tests confirm selection persistence and backend validation.
- `bun test` and `uv run pytest` executed.

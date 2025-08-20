# Persist active run across reloads

## Context
- Refreshing the site always starts a new run; the frontend does not remember ongoing runs.
- `frontend/src/routes/+page.svelte` initializes `runId` to an empty string and never checks for a previous value.

## Task
1. Store `runId` (and any required room state) in `localStorage` whenever a run starts or advances to a new room.
2. On page load, read the stored `runId` and verify it with the backend (e.g., fetch `/map/{runId}`); if valid, restore `runId` and current room data instead of starting a new run.
3. Provide a cleanup path that removes stored values when the run ends or verification fails.
4. Add a frontend test that simulates a stored `runId` and confirms `GameViewport` resumes the existing run after a page refresh.
5. Run `bun test` and `uv run pytest` after implementing.

## Acceptance Criteria
- Reloading the page during an active run resumes that run rather than creating a new one.
- New test demonstrates run persistence.
- `bun test` and `uv run pytest` executed.

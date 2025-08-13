# Lock player stat editing during runs

## Summary
The player editor refuses stat or pronoun changes when a run is active. The
backend checks the `runs` table before applying updates so mid-run stats remain
fixed.

## Acceptance Criteria
- `PUT /player/editor` returns an error if any run record exists.
- Edits succeed again once no active runs are stored.

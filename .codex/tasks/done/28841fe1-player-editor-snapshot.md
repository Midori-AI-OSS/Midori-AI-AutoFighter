# Persist player edits and snapshot on run start (`28841fe1`)

## Summary
The backend blocks player editor saves during an active run, causing edits to be lost. Allow edits to persist regardless and snapshot player state when starting a new run.

## Tasks
- [x] Remove the active-run guard in `/player/editor` so stats and settings always save.
- [x] When a run begins, clone the current player record to the run instance so later edits don't affect the active run.
- [x] Add regression tests verifying that edits persist and runs use the snapshot.

## Context
User reports indicate that player customization changes revert during runs. The new workflow should decouple persistent data from run-specific state.

## Notes
Coordinate with existing player editor and save system docs. Ensure documentation reflects the snapshot behavior.

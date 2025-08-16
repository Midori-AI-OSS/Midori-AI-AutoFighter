# Fix framerate persistence bug (`15f0b90b`)

## Summary
Selecting a framerate and saving resets the value instead of persisting it.

## Tasks
- [x] Reproduce the framerate reset in the settings workflow.
- [x] Correct the save and load path so the chosen framerate is stored.
- [x] Add a regression test verifying persistence across sessions.

## Context
Feedback reports that backend polling frequency cannot be changed due to this bug.

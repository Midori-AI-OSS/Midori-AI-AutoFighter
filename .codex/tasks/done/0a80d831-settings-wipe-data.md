# Fix settings wipe data (`0a80d831`)

## Summary
The Settings screen's "wipe data" option fails to clear user progress or local save files.
Fixed so the `/save/wipe` endpoint removes runs, options, and damage type entries from the backend database as well as local settings.

## Tasks
- [x] Review the current wipe-data handler and ensure it deletes saves, caches, and local storage.
- [x] Implement missing deletion logic and update UI to reflect a fresh state after wiping.
- [x] Prompt for confirmation before wiping and show a success message when complete.
- [x] Add tests verifying that data is removed and a new game starts cleanly.
- [x] Document the wipe-data flow and testing steps in the settings docs.

## Context
Feedback reports that tapping "wipe data" does nothing, preventing users from resetting progress.

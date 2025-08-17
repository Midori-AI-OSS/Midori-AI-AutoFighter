# Fix Player Editor stat save (`695bf9b6`)

## Summary
Stat edits in the Player Editor revert to 0 after saving or closing.

## Tasks
- [x] Trace the save flow from UI to persistence for stat values.
- [x] Ensure edited stats persist across saves and reloads.
- [x] Document reproduction steps and add tests.

## Context
Feedback reports that player customization is currently broken.

## Notes
Mapped `damage_type` to `damageType` in the UI and dispatched numeric stat
values so the backend persists them correctly. Added doc notes and a regression
test.

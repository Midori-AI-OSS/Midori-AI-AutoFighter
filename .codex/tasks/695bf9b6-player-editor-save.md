# Fix Player Editor stat save (`695bf9b6`)

## Summary
Stat edits in the Player Editor revert to 0 after saving or closing.

## Tasks
- [ ] Trace the save flow from UI to persistence for stat values.
- [ ] Ensure edited stats persist across saves and reloads.
- [ ] Document reproduction steps and add tests.

## Context
Feedback reports that player customization is currently broken.

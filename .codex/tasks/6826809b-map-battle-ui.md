# Improve map and battle UI (`6826809b`)

## Summary
Map scrolling and battle interface suffer from missing assets and layout problems.

## Tasks
 - [ ] Clip or paginate the map to show only the next four room groups.
 - [ ] Theme the rewards menu and hide sidebars during battles.
 - [ ] Ensure the battle background renders inside the battle viewport.
 - [ ] Reuse the shared character asset loader so party member icons and damage type colors display correctly.
 - [ ] Refactor battle layout to prevent overlapping elements and sidebar bleed.
 - [ ] Capture DOM and network logs on battle start and add tests verifying asset loading and layout.

## Context
Feedback outlines scrolling and UI glitches in map and battle scenes.

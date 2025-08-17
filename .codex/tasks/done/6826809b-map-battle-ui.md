# Improve map and battle UI (`6826809b`)

## Summary
Map scrolling and battle interface suffer from missing assets and layout problems.

## Tasks
- [x] Clip or paginate the map to show only the next four room groups.
- [x] Reduce rendered DOM nodes for the map to improve performance.
- [x] Theme the rewards menu and hide sidebars during battles.
- [x] Ensure the battle background renders inside the battle viewport.
- [x] Reuse the shared character asset loader so party member icons and damage type colors display correctly.
- [x] Refactor battle layout to prevent overlapping elements and sidebar bleed.
- [x] Capture DOM and network logs on battle start and add tests verifying asset loading and layout.

## Context
Feedback outlines scrolling and UI glitches in map and battle scenes.

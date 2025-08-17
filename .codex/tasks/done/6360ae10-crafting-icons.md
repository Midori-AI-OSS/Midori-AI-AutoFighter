# Restore crafting menu icons (`6360ae10`)

## Summary
Crafting list shows item names and counts but lacks icons and star-rank outlines.

## Tasks
- [x] Verify asset paths and rendering logic for crafting item icons and star-rank outlines.
- [x] Audit CSS rules that may hide icons or outlines.
- [x] Ensure icon and outline layers stack correctly.
- [x] Build a two-pane layout: list container ~80% width and detail panel ~18% showing clicked item info.
- [x] Add star-rank outlines and a fallback placeholder icon when assets fail to load.
- [x] Document asset locations and relevant CSS in the crafting docs.

## Context
Feedback.md item 2 reports that the crafting list shows names without icons or star-rank outlines, likely due to bad asset paths or CSS hiding sprites. This task restores those visuals and adds a placeholder when files are missing.

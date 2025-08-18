# Ensure reward card art loads (`0a8d3663`)

## Summary
Card art fails to appear on the reward screen, likely due to filename mismatches or missing assets. A random card should display with correct art or fallback each time.

## Tasks
- Audit reward card filenames and asset paths; correct any mismatches that prevent images from loading.
- Confirm the reward screen selects a random card and renders its associated image.
- Ensure the existing fallback art displays whenever a card image is missing.
- Add frontend tests that open the reward screen repeatedly to verify card art or fallback renders without errors.
- Tint cards according to their star rank so rarities have distinctive overlays.
- Update asset-loading documentation in `.codex/instructions/asset-loading.md` if paths or naming conventions change.

## Context
Feedback item 5 reports missing card art on the reward screen.

Status: Need Review

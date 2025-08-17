# Fix party and character picker issues (`2f1f575c`)

## Summary
Party and character pickers show incorrect types, stat placement, colors, layout, and roster contents after data wipes.

## Tasks
- [x] Ensure Player Editor settings persist so party picker shows correct player type.
- [x] Hide characters that are no longer owned after a data wipe.
- [x] Move DEF to the top of the Defense tab and EXP beneath HP in the Core tab.
- [x] Correct type icon color and outline color in the character picker.
- [x] Display one character per row for better readability.
- [x] Audit CSS grid and layout to prevent overlapping elements or multi-character rows.
- [x] Add tests verifying stat positions, type assignments, and absence of wiped characters.
- [x] Capture DOM snapshots confirming correct layout and color mapping.

## Context
Feedback identifies multiple UI and data inconsistencies in these pickers.

# Add post-fight loot summary screen (`dec21443`)

## Summary
After each battle, show a dedicated loot screen summarizing gained gold, cards, relics, and items. This screen should host the "Next Room" control so runs only advance after review.

## Tasks
- [x] Create backend response that lists all loot awarded at battle end.
- [x] Build a frontend loot summary overlay showing gold, cards, relics, and other drops.
- [x] Move "Next Room" button to this screen and gate backend progression until it is pressed.
- [x] Include relic picker if a relic drop occurs.
- [x] Document the post-fight flow and loot display.

## Context
Loot currently appears immediately with no chance to review; a summary screen clarifies rewards and unifies progression with the next-room trigger.

Status: Need Review


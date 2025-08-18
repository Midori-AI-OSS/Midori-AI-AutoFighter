# Resize reward screen to card grid (`4c06ac25`)

## Summary
The reward overlay renders much larger than the card choices. It should match the footprint of a 1x3 card grid now and scale to a 2x3 grid in the future.

## Tasks
- Constrain the reward screen container's width and height to the combined footprint of the displayed cards, removing excess padding.
- Implement responsive CSS that supports the current 1x3 grid and scales cleanly to a 2x3 grid when more cards are offered.
- Ensure the overlay remains centered within the battle viewport and does not block sidebar elements.
- Verify the layout against varying screen sizes and card counts.
- Add frontend tests verifying reward screen dimensions for both 3-card (1x3) and 6-card (2x3) scenarios.
- Update reward UI documentation in `.codex/instructions/battle-room.md` to detail sizing rules and grid expansion.

## Context
Feedback item 4 notes that the reward screen is oversized relative to its card contents.

Status: Need Review

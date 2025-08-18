# Restore top bar with battle icon (`24d1f2bf`)

## Summary
The top-left navigation bar disappears during battles, removing the home button. When a battle is active, the bar should remain and show a battle icon instead of the home icon.

## Tasks
- Keep the top navigation bar rendered on the battle screen by adjusting layout or visibility styles.
- Swap the home button for a battle icon while combat is active and revert back once the battle ends.
- Use existing battle icon assets and ensure clicking the icon does not navigate away from the ongoing fight.
- Integrate the icon toggle with existing routing logic so home navigation is restored outside battles.
- Add frontend tests verifying bar visibility and icon toggling before, during, and after combat.
- Update relevant UI documentation in `.codex/instructions/battle-room.md` or `main-menu.md` with the new behavior.

## Context
Feedback item 3 notes the missing top-left bar during battles and requests a battle-specific icon.

Status: Need Review

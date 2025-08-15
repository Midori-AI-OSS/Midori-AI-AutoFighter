# Lock Menus During Active Battles

## Summary
Front end should detect when a battle is running on the backend and restrict access to menus other than Settings.

## Instructions
- Poll backend to see if a battle is active when menus open.
- If fighting, show battle screen or resume state and disable other menus except Settings.
- Re-enable menus once the battle ends.

## Context
Prevents players from bypassing combat and keeps UI in sync with backend battles.

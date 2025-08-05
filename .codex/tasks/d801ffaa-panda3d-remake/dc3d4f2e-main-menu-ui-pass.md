# Main Menu UI Pass

## Summary
Audit and fix the main menu, especially the New Run flow, to resolve scaling issues and eliminate prototype code.

## Tasks
- [ ] Reproduce and fix New Run menu bugs.
- [ ] Standardize DirectGUI scale values across all menus.
- [ ] Show a character picker before runs start, even if no characters exist, letting players choose damage type and melee or spellcaster roles.
- [ ] Display the floor map after setup so players can select a route instead of entering a fight immediately.
- [ ] Remove placeholder or prototyping code from menu implementation.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
Recent feedback shows the New Run and settings menus render at inconsistent scales and rely on temporary code.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
status: in progress

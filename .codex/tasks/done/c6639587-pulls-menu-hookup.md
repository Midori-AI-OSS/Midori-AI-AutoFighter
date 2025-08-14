# Hook up pulls menu

## Summary
Expose a Pulls menu and connect it to backend gacha endpoints.

## Tasks
- Add a Pulls button that opens the gacha interface.
- Call `/gacha/pull` and display results with pity and currency updates.

## Context
Players cannot access gacha recruitment from the main menu.

## Notes
Share pity and currency with rest-node access.

## Outcome
Pulls button opens `PullsMenu`, which fetches gacha state, shows pity and ticket counts, and updates the list of results after each pull.

# Note automatic saving on total party defeat

## Summary
Ensure documentation explains that the game saves player states automatically once every fighter has fallen.

## Details
- Add a sentence to the game workflow section clarifying that when all players die, their latest states are written back to `lives/` and the application exits.
- Include a reminder that no manual action is required; saving occurs even if the window is closed after defeat.
- Provide a brief example of the saved file paths to reinforce understanding.

## Notes
- Based on `.codex/tasks/e293d9ef-document-game-workflow.md`.

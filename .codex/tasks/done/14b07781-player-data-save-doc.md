# Document player data persistence

## Summary
Explain where and how player progress is stored so contributors understand the save system.

## Details
- Note that each fighter's state is serialized to `lives/<player>.dat` at the end of a run.
- Mention that combat logs for each player are appended to `logs/<player>.txt` during play.
- Include guidance on the format or encoding of the `.dat` files if known, or state that it uses Python's built-in serialization.
- Ensure this information is placed alongside the game workflow documentation.

## Notes
- Based on `.codex/tasks/e293d9ef-document-game-workflow.md`.

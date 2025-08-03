# Outline game loading, wave progression, and run termination

## Summary
Create documentation that walks readers through the game's runtime sequence from initial plugin loading to the point where all fighters fall and the run ends.

## Details
- Describe how `PluginLoader` initializes and restores fighters from `lives/<name>.dat` files at launch.
- Explain how waves of foes are spawned, including how experience and levels are gained automatically.
- Clarify that the game concludes when every player character is defeated.
- Indicate where in the docs this narrative should live (e.g., `README.md` or `.codex/implementation/game-workflow.md`).

## Notes
- Based on `.codex/tasks/e293d9ef-document-game-workflow.md`.

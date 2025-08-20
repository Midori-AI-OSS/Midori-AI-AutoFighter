# Improve battle stats readability

## Context
- Players report that stat text during battles is difficult to read against the background.
- Navigation elements use a stained-glass theme (`.stained-glass-bar`, `.stained-glass-side` in `frontend/src/lib/GameViewport.svelte`) and the UI plan (`.codex/planning/e26e5ed7-ui-foundation-plan.md`) calls for frosted glass surfaces with high contrast text.
- `frontend/src/lib/BattleView.svelte` currently renders stats directly over the battlefield without any container or theme.

## Task
1. Wrap the party and foe stat sections in `BattleView.svelte` with resizable stained-glass containers that match the top-left bar and right sidebar styling.
2. Reuse or extract shared stained-glass styles so both containers use consistent gradients, borders, and backdrop blur.
3. Ensure the containers adjust to viewport size, keeping portraits and HP bars visible while improving text contrast.
4. Update CSS and layout to prevent overlap with existing elements and keep readability on desktop and mobile.
5. Add a frontend test verifying that the new container classes render for both party and foe columns.
6. Run `bun test` and `uv run pytest` after changes.

## Acceptance Criteria
- Stats for both allies and foes appear within stained-glass containers and remain legible across screen sizes.
- New test confirms containers render.
- `bun test` and `uv run pytest` executed.

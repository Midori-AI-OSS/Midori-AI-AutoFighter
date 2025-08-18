# Reward Overlay

After a battle resolves, the backend may return `card_choices`. `GameViewport.svelte` detects these and opens `RewardOverlay.svelte` inside an `OverlaySurface`. The overlay wraps its options in `MenuPanel` for consistent theming and loads art from `src/lib/assets` rather than the `.codex` downloads. Card rewards display a random gray background tinted to the card's star rank with the name overlaid at the top. Clicking a choice opens a status panel below with the card's description and a confirm button so players can verify their selection. Relic and item rewards reuse the same component and asset pipeline.

Selecting a card posts to `/cards/<run_id>` via the `chooseCard` API helper once the player confirms, clearing `card_choices` so the run can proceed to the next room.

## Testing
- `bun test frontend/tests/rewardoverlay.test.js`

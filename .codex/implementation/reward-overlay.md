# Reward Overlay

After a battle resolves, the backend returns a `loot` object summarizing gold and any reward options. `GameViewport.svelte` now always shows `RewardOverlay.svelte` after battles, passing along `card_choices`, `relic_choices`, and the gold gain. The overlay wraps its options in `MenuPanel` for consistent theming and loads art from `src/lib/assets` rather than the `.codex` downloads. Card rewards display a random gray background tinted to the card's star rank with the name overlaid at the top. Clicking a choice opens a status panel below with the card's description and a confirm button so players can verify their selection. Relic and item rewards reuse the same component and asset pipeline.

Selecting a card posts to `/cards/<run_id>` via the `chooseCard` API helper once the player confirms, clearing `card_choices`. A disabled "Next Room" button is shown at the bottom of the overlay until all selections are resolved. When the player clicks it, the frontend calls `/run/<id>/next` to advance the map.

## Testing
- `bun test frontend/tests/rewardoverlay.test.js`

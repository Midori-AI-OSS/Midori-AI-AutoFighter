# Reward Overlay

After a battle resolves, the backend returns a `loot` object summarizing gold and any reward options. `GameViewport.svelte` keeps `BattleView` mounted and stops its polling loop so the last snapshot remains visible. A `PopupWindow` inside `OverlaySurface` then presents `RewardOverlay.svelte`, which receives the battle's `card_choices`, `relic_choices`, and gold gain. The reward popup loads art from `src/lib/assets` and displays card options with a gray background tinted to the card's star rank and the name overlaid at the top. Clicking a choice opens a status panel below with the card's description and a confirm button so players can verify their selection. Relic and item rewards reuse the same component and asset pipeline.

Selecting a card posts to `/cards/<run_id>` via the `chooseCard` API helper once the player confirms, clearing `card_choices`. The "Next Room" button remains disabled until all selections are resolved. Clicking it dismisses the popup, unmounts `BattleView`, and calls `/run/<id>/next` to advance the map.

## Testing
- `bun test frontend/tests/rewardoverlay.test.js`

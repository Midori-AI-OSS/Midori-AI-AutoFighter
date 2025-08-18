# Post-Fight Loot Screen

After a battle concludes the backend responds with a `loot` object summarizing gold earned and any reward choices. `GameViewport.svelte` always opens `RewardOverlay.svelte` to display this information. Players must resolve any card or relic picks and then press the **Next Room** button, which calls `/run/<id>/next` to advance the run.

## Testing
- `uv run pytest tests/test_loot_summary.py`
- `bun test`

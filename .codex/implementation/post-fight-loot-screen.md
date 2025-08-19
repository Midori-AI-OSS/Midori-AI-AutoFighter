# Post-Fight Loot Screen

After a battle concludes the frontend polls `roomAction(runId, 'battle', 'snapshot')` until the snapshot includes a `loot` object summarizing gold earned and any reward choices. `GameViewport.svelte` keeps `BattleView.svelte` mounted during this polling and only opens `RewardOverlay.svelte` once the `loot` data arrives and combat is flagged complete. Players must resolve any card or relic picks and then press the **Next Room** button, which calls `/run/<id>/next` to advance the run.

## Testing
- `uv run pytest tests/test_loot_summary.py`
- `bun test`

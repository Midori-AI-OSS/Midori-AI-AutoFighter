# Player Editor

`PlayerEditor` now connects to backend endpoints and is launched from the main
menu's **Edit** button or automatically before a run, so players can set custom
pronouns up to 15 characters, pick a starting damage type—Light, Dark, Wind,
Lightning, Fire, or Ice—and allocate stat points before starting a run.

- Players start with 100 base points and may gain bonus points from owning 100 of each damage type's 4★ upgrade items.
- Sliders for HP, Attack, and Defense clamp so the sum never exceeds the available pool.
- Each point grants a 1% multiplier to the chosen stat, doubling it at 100 points.
- A label displays remaining points.
- The Confirm button is disabled until the 100 base points are spent. Bonus points are optional and unspent amounts stay in the inventory.
- Attempting to spend more points than covered by 4★ items shows a warning and prevents saving. Backend `PUT /player/editor`
  also enforces the 100-point cap and rejects edits while a run is active.

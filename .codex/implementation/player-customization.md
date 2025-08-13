# Player Editor

`PlayerEditor` is currently a placeholder in the frontend. It will eventually
let players set custom pronouns up to 15 characters, pick a starting damage
type—Light, Dark, Wind, Lightning, Fire, or Ice—and allocate stat points before
starting a run.

- Players start with 100 base points and may gain bonus points from owning 100 of each damage type's 4★ upgrade items.
- Sliders for HP, Attack, and Defense clamp so the sum never exceeds the available pool.
- A label displays remaining points.
- The Confirm button is disabled until the 100 base points are spent. Bonus points are optional and unspent amounts stay in the inventory.
- Attempting to spend more points than covered by 4★ items shows a warning and prevents saving.

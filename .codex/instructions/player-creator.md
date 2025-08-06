# Player Creator

The Player Creator scene lets users customise their fighter before starting a run.

## Appearance
- Choose a body style: Athletic, Slim, or Heavy
- Choose a hair style: Short, Long, or Ponytail
- Pick a hair color: Black, Blonde, or Red
- Select an accessory: None, Hat, or Glasses

## Stats
Distribute 100 points across HP, Attack, and Defense using sliders. Spending 100 of each damage type's 4★ upgrade items grants one extra point. Optional bonuses from starter items are added when confirming the selection.

## Saving
Confirming writes the chosen appearance and stats to `player.json`, which is loaded when starting a new run.

## Layout
Widget positions and scales are computed from the current window size via `gui.get_normalized_scale_pos`.  Add new widgets to the `_responsive` list in `PlayerCreator` to keep them updating on resize.

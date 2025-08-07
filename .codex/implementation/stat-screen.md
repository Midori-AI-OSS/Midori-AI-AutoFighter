# Stat Screen Implementation

Provides an in-game overlay for grouped statistics and active status effects.

## Rendering
- Creates a transparent `DirectFrame` that fills the screen.
- Renders grouped lines for Core, Offense, Defense, Vitality & Advanced, and Status categories using `OnscreenText` anchored left.
- Registers an Escape key handler to close the screen via the scene manager.
- `add_status_hook` allows modules to append extra status lines during rendering.

## Refresh Rate
- Uses the application's `stat_refresh_rate` attribute by default and accepts an optional override.
- Refresh interval clamps to the 1–10 range and triggers a re-render on every `refresh_rate` ticks of the Panda3D task manager.

## Pausing
- When `pause_on_stats` is enabled on the app, opening the stat screen calls `pause_game` and closing it resumes.


# Settings Menu

The `SettingsMenu` component groups options into **Audio**, **Gameplay**, and
**Server** sections inside a shared `MenuPanel`. Sliders adjust sound, music,
and voice volumes; a dropdown toggles between Light, Dark, or Editable themes;
and a **Frame Rate Cap** selector offers 30, 60, or 120 FPS. The backend polling
rate derives from the selected cap (`1000 ÷ fps`). The menu auto-saves whenever a
value changes and exposes a single **Close** button to exit.

## Testing
- `bun test`

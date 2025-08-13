# Settings Menu

The `SettingsMenu` component provides volume sliders for sound, music, and
voice. It renders within the shared `OverlaySurface` so the panel fills the
viewport beneath the stained-glass bar and scales with the window. The
surface clips overflow, so the menu's container uses flexible sizing to stay
just inside the available space without triggering scrollbars.

Selecting **Settings** from the main menu or in-game toolbar opens this menu.
Changes are not persisted yet; both **Confirm** and **Cancel** close the menu.

## Testing
- `bun test`

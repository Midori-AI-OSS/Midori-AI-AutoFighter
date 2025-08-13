# Menu Panel

`MenuPanel.svelte` provides a shared container for full-screen menus. It
occupies roughly 99% of the overlay surface, applies consistent padding,
border, and backdrop blur, and sets `overflow: auto` so content scrolls
inside the game viewport. Menus such as `PartyPicker` and `SettingsMenu`
wrap their inner layout with this component to guarantee a consistent,
resizable format.

## Testing
- `bun test`

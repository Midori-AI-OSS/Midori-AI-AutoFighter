# Settings Menu

`SettingsMenu.svelte` now follows the options spec. It includes Lucide icons,
labels, and tooltips for **SFX Volume**, **Music Volume**, **Voice Volume**,
**Framerate**, and an **Autocraft** toggle. Buttons for speed and pause sit in
the game viewport's top-right corner to access this menu. Controls are grouped
under **Audio**, **System**, and **Gameplay** headings for clarity.

The selected framerate is saved as a number and merged with existing settings in local storage so server polling limits persist across sessions.

## Testing
- `bun test`

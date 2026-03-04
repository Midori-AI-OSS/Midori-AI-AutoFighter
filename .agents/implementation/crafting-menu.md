# Crafting Menu

The standalone crafting interface has been removed. Upgrade materials now
appear in `InventoryPanel.svelte`, which presents a color‑coded grid with
quantity badges and a detail pane. Manual `/gacha/craft` calls are no longer
exposed in the UI; auto‑crafting can be toggled from the Settings menu.

## Testing
- `bun test`


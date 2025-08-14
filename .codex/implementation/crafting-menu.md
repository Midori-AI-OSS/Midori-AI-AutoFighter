# Crafting Menu

`CraftingMenu.svelte` fetches upgrade items from `/gacha`, lists their counts,
and lets players convert materials via `/gacha/craft`. A checkbox toggles
automatic crafting by calling `/gacha/auto-craft`, and a **Craft** button runs a
manual upgrade pass. The menu appears from both the main menu and rest rooms
using the shared `MenuPanel` style.

## Testing
- `bun test`

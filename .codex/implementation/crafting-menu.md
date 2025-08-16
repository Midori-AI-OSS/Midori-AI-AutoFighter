# Crafting Menu

`CraftingMenu.svelte` fetches upgrade items from `/gacha`, lists their counts,
and lets players convert materials via `/gacha/craft`. A checkbox toggles
automatic crafting by calling `/gacha/auto-craft`, and a **Craft** button runs a
manual upgrade pass. The menu appears from both the main menu and rest rooms
using the shared `MenuPanel` style.

Each item displays a 24×24 icon sourced from
`frontend/src/lib/assets/items/{element}/generic{rank}.png`. The image border
color reflects star rank (gray→gold for 1–5★) via the `--star-color` CSS
variable and falls back to
`frontend/src/lib/assets/cards/fallback/placeholder.png` if an icon is missing.

## Testing
- `bun test`

# Crafting Menu

`CraftingMenu.svelte` fetches upgrade items from `/gacha`, lists their counts,
and lets players convert materials via `/gacha/craft`. A checkbox toggles
automatic crafting by calling `/gacha/auto-craft`, and a **Craft** button runs a
manual upgrade pass. The menu appears from both the main menu and rest rooms
using the shared `MenuPanel` style.

Items are stacked by element and star rank using `stackItems` so identical
materials collapse into a single entry with an updated count. Names are
normalized via `formatName` (e.g., `ice_4` → `Ice ★★★★`) for readability.

Each entry displays a 24×24 icon sourced from
`frontend/src/lib/assets/items/{element}/generic{rank}.png`. The image border
color reflects star rank (gray→gold for 1–5★) via the `--star-color` CSS
variable and falls back to
`frontend/src/lib/assets/cards/fallback/placeholder.png` if an icon is missing.
Clicking an item highlights a side detail panel showing a 48×48 icon, name, and
count. The menu uses a two-pane grid with the item list taking ~80% width and
the detail view ~18% so players can inspect a material without losing their
place.

## Testing
- `bun test`

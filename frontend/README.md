# Frontend

Svelte-based GUI served with Bun on port `59001`.

## Setup

```bash
cd frontend
bun install
bun dev
```

The development server runs at `http://localhost:59001` and displays a
high-contrast icon grid powered by `lucide-svelte`. Clicking **Party** opens a
responsive party picker overlay that fetches available characters from the
backend and lets you add or remove allies with a single button. Portraits
use four equal columns so each image scales to 25% of the roster width, and
no confirm action is required. The **Run** icon posts the selected party to
`/run/start` and reveals the generated floor map. The **Settings** icon opens a
similar overlay with sliders for sound effects, music, and voice that auto-save changes and briefly show a "Saved" status. An upcoming **Edit Player** panel will use
`/player/editor` to save pronouns, starting damage type, and stat allocations,
boosting HP, Attack, and Defense by 1% per point.
The **Pulls** icon calls `/gacha/pull` so players can recruit 5★ or 6★ characters or
earn 1★–4★ upgrade items between runs. Pity raises the odds of higher-tier items,
and auto-crafting those materials is an optional toggle. A **Craft** icon opens a
menu listing upgrade items, offering a manual `/gacha/craft` action and a toggle
for `/gacha/auto-craft`. A **Feedback** icon opens a pre-filled GitHub issue in a new tab so players can report bugs or sugges
tions.
After each battle, any returned `card_choices` trigger a reward overlay that
loads art from `src/lib/assets` and lets the player pick one before
continuing. During combat, party members appear in a left column and foes on the right, with HP, Attack, Defense, Mitigation, and Crit rate listed beside each portrait. HoT/DoT markers render below each portrait and collapse duplicate effects into a single icon with a small stack count in the bottom-right corner.

Placeholder icons for items, relics, and cards live under `src/lib/assets/{items,relics,cards}`. Each damage type or star rank has its own folder with 24×24 colored placeholders so artists can replace them later.

## Settings: Wipe Save Data
- The Wipe button calls the backend wipe endpoint and also clears all client storage and caches (localStorage, sessionStorage, IndexedDB, CacheStorage) and unregisters service workers. After completion it forces a full page reload to prevent stale roster or party selections from persisting.

## Asset Loading
- Backgrounds: a random image is selected from `src/lib/assets/backgrounds` whenever the viewport initializes.
- Character portraits: if `src/lib/assets/characters/<name>.png` exists it is used; otherwise if a folder `src/lib/assets/characters/<name>/` exists, a random `.png` inside that folder is used. If neither exists, a random fallback from `src/lib/assets/characters/fallbacks` is used, falling back to the Midori AI logo as a last resort.

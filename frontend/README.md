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
similar overlay with sliders for sound effects, music, and voice. An upcoming **Edit Player** panel will use
`/player/editor` to save pronouns, starting damage type, and stat allocations,
boosting HP, Attack, and Defense by 1% per point.
The **Pulls** icon calls `/gacha/pull` so players can recruit 5★ or 6★ characters or
earn 1★–4★ upgrade items between runs. Pity raises the odds of higher-tier items,
and auto-crafting those materials is an optional toggle. A **Craft** icon opens a
menu listing upgrade items, offering a manual `/gacha/craft` action and a toggle
for `/gacha/auto-craft`. A **Feedback** icon opens a pre-filled GitHub issue in a new tab so players can report bugs or sugges
tions.
During a run, `MapDisplay.svelte` shows the path with the boss at the top and
the current room highlighted at the bottom. Future rooms remain visible but are
greyed out and disabled. Selecting the highlighted room posts `{ "action": "" }`
to `/rooms/<run_id>/<type>` and refreshes the map from the backend.

After each battle, any returned `card_choices` trigger a reward overlay that
pulls art from `.codex/downloads` and lets the player pick one before
continuing.

Placeholder icons for items, relics, and cards live under `src/lib/assets/{items,relics,cards}`. Each damage type or star rank has its own folder with 24×24 colored placeholders so artists can replace them later.

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
similar overlay with volume sliders. An upcoming **Edit Player** panel will use
`/player/editor` to save pronouns, starting damage type, and stat allocations,
boosting HP, Attack, and Defense by 1% per point.
The **Pulls** icon calls `/gacha/pull` so players can recruit 5★ or 6★ characters or
earn 1★–4★ upgrade items between runs. Pity raises the odds of higher-tier items,
and auto-crafting those materials is an optional toggle.
During a run, `MapDisplay.svelte` shows upcoming rooms as stained-glass buttons
with matching `lucide-svelte` icons.


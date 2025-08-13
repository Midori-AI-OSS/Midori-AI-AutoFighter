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
no confirm action is required. The **Settings** icon opens a similar overlay
with volume sliders.


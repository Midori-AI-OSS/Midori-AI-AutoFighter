# Responsive Layout

The Svelte frontend adapts the interface to three viewport ranges:

- **Desktop (≥1024px)** – shows the main menu beside the party picker panel.
  Player editor and stats panels are planned but currently hidden.
- **Tablet (600–1023px)** – shows the main menu beside the party picker for a two-panel view.
- **Phone (<600px)** – focuses on a single menu at a time for clarity on small screens.

## Testing
- `layoutForWidth` maps breakpoints and `panelsForWidth` lists visible panels.
- `cd frontend && bun test`

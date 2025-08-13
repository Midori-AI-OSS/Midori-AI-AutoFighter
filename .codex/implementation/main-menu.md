# Main Menu

The Svelte front page presents a high-contrast grid of icon buttons inspired by
Arknights. Menu items include **Run**, **Party**, **Settings**, and **Stats**, each
showing a Lucide icon above a label. **Settings** opens its own overlay within the
viewport using the shared menu surface. Layout is determined by `layoutForWidth`:
- **Desktop:** menu grid with the PartyPicker panel alongside it. PlayerEditor
  and StatsPanel are planned but not displayed yet.
- **Tablet:** menu grid beside the PartyPicker panel.
- **Phone:** only the menu grid is shown for clarity.

Choosing **Run** opens the PartyPicker overlay to review the lineup before a run.

## Testing
- `bun test frontend/tests/layout.test.js`

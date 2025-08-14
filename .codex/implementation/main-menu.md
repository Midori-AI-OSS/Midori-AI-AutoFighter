# Main Menu

The Svelte front page presents a high-contrast grid of icon buttons inspired by
Arknights. Menu items include **Run**, **Map**, **Party**, **Edit**, **Pulls**,
**Craft**, **Settings**, and **Stats**, each showing a Lucide icon above a label.
**Craft** opens a menu to upgrade items and toggle auto-crafting. **Settings**
opens its own overlay within the viewport using the shared menu surface. Layout is
determined by `layoutForWidth`:
- **Desktop:** menu grid with the PartyPicker panel alongside it. StatsPanel is
  planned but not displayed yet.
- **Tablet:** menu grid beside the PartyPicker panel.
- **Phone:** only the menu grid is shown for clarity.

Choosing **Run** opens the PartyPicker overlay to review the lineup before a run.
Selecting **Map** fetches the current run's layout and displays it in
`MapDisplay`. **Edit** retrieves the player's configuration and launches the
`PlayerEditor` for pronoun, damage-type, and stat tweaks. **Pulls** opens a
gacha panel that shows the current pity counter and updates currency and
results after invoking `/gacha/pull`.

## Testing
- `bun test frontend/tests/layout.test.js`

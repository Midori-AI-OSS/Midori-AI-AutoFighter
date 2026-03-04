# Party Picker

The Svelte `PartyPicker` component lets players choose up to four allies before a run. The shared `assetLoader` picks a random background from `frontend/src/lib/assets/backgrounds`, provides portraits from `assets/characters` with fallbacks, and supplies damage type icons and colors via `getElementIcon` and `getElementColor`.

`PartyPicker` now composes three focused child components:

- **`PartyRoster`** – lists owned characters and handles selection. Rows tint the outline and element icon with `getElementColor` for quick damage-type recognition. Selection uses two-way binding on `previewId` so the parent can preview or modify the party.
- **`PlayerPreview`** – shows a large portrait of the currently selected character or a placeholder message when none is chosen.
- **`StatTabs`** – renders a tabbed stats panel (Core, Offense, Defense) and embeds a reusable **`CharacterEditor`** for both players and NPCs. Sliders allow adjusting HP, Attack, Defense, Crit Rate, and Crit Damage, with player changes auto‑saved via the backend. A **Add to party** / **Remove from party** toggle is exposed via a `toggle` event.

The layout uses percentage-based columns so the roster, preview, and stats panels all shrink with the viewport. Content is wrapped in `MenuPanel`, which sizes itself just under the overlay surface to avoid a surrounding scrollbar. Preview portraits scale without a minimum size so they remain visible on small screens.

`PartyPicker` exposes the `selected` array as a bound prop so parents can reactively read the lineup. When launched from the Run button it opens as a modal that requires an explicit **Start Run** confirmation before proceeding.

`startRun` in `frontend/src/lib/api.js` posts the chosen party and optional player damage type to the Quart backend's `/run/start` endpoint, which validates ownership and returns run data with passive names.

Upon success, the parent page stores the `run_id` and initial map and immediately switches to the map view so the run can begin.

The confirmation footer wraps **Start Run** and **Cancel** in a stained-glass row so these buttons match the rest of the interface.

## Testing
- `bun test frontend/tests/partypicker.test.js`

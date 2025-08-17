# Party Picker

The Svelte `PartyPicker` component lets players choose up to four allies before a run. The shared `assetLoader` picks a random background from `frontend/src/lib/assets/backgrounds`, provides portraits from `assets/characters` with fallbacks, and supplies damage type icons and colors via `getElementIcon` and `getElementColor`.

The roster only shows owned characters plus the player's avatar, which is pinned to the top and preselected. Any characters removed by a data wipe are filtered from both the roster and the current selection. Entries render one per row with a small portrait, name, and element icon. Each row's outline and icon are tinted with `getElementColor` so damage types are visible at a glance. Clicking a row previews the character without toggling party membership. The stats panel provides an **Add to party** / **Remove from party** control.

The layout uses percentage-based columns so the roster, preview, and stats
panels all shrink with the viewport. Content is wrapped in `MenuPanel`,
which sizes itself just under the overlay surface to avoid a surrounding
scrollbar. Preview portraits scale without a minimum size so they remain
visible on small screens.

Player stats are grouped into Core, Offense, and Defense tabs. The Core tab
lists HP, EXP, Vitality, and Regain. The Defense tab begins with DEF
followed by Mitigation, Dodge Odds, and Effect Resist.

`PartyPicker` exposes the `selected` array as a bound prop so parents can reactively read the lineup. When launched from the Run button it opens as a modal that requires an explicit **Start Run** confirmation before proceeding.

`startRun` in `frontend/src/lib/api.js` posts the chosen party and optional player damage type to the Quart backend's `/run/start` endpoint, which validates ownership and returns run data with passive names.

Upon success, the parent page stores the `run_id` and initial map and immediately
switches to the map view so the run can begin.

The confirmation footer wraps **Start Run** and **Cancel** in a stained-glass row so these buttons match the rest of the interface.

## Testing
- `bun test frontend/tests/partypicker.test.js`

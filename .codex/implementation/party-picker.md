# Party Picker

The Svelte `PartyPicker` component lets players choose up to four allies before a run. A random background image is selected from `frontend/src/lib/assets/backgrounds`, and portraits load from `assets/characters` with a fallback to a random portrait when an image is missing.

The roster only shows owned characters plus the player's avatar, which is pinned to the top and preselected. The list scrolls vertically with a gradient fade at the top and bottom. Clicking a portrait now only previews the character. Party membership is managed with a button in the stats panel that switches between **Add to party** and **Remove from party**.

The layout uses percentage-based columns so the roster, preview, and stats
panels all shrink with the viewport. Roster portraits fill a four‑column
grid where each card spans **25%** of the available width, keeping images a
constant ratio of the menu. Content is wrapped in `MenuPanel`, which sizes
itself just under the overlay surface to avoid a surrounding scrollbar.
Preview portraits scale without a minimum size so they remain visible on
small screens.

`PartyPicker` exposes the `selected` array as a bound prop so parents can reactively read the lineup. When launched from the Run button it opens as a modal that requires an explicit **Start Run** confirmation before proceeding.

`startRun` in `frontend/src/lib/api.js` posts the chosen party and optional player damage type to the Quart backend's `/run/start` endpoint, which validates ownership and returns run data with passive names.

## Testing
- `bun test frontend/tests/partypicker.test.js`

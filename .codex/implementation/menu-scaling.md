# Menu Overlay and Resizing

Menus render inside the game viewport beneath the stained‑glass top bar.
All full-screen menus (e.g., `PartyPicker`, `SettingsMenu`) sit inside the
`OverlaySurface` component. The surface fills the remaining space and clips
its own overflow so individual menus must handle scrolling. To prevent stray
scrollbars, a menu’s root container should size itself just under the
surface dimensions (around 99% of width and height) and use flexible
units so panels and portraits shrink with the viewport. Avoid fixed widths
or implicit minimums by applying `min-width: 0` to grid and flex items that
need to collapse. Grids that display cards should define tracks in
percentages (e.g., `repeat(auto-fill, minmax(0, 25%))` for four columns) so
elements stay proportional to the menu.

## Testing
- `bun test`

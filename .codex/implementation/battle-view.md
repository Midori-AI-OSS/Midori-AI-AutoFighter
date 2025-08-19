# Battle View

`BattleView.svelte` renders turn-based encounters inside `MenuPanel`. It draws a
random backdrop from the shared `assetLoader` and displays the party and foes in
opposing columns. Portraits are now 6 rem square for better visibility and sit
beneath Pokémon-style HP bars that track current health.

Each combatant lists HP, ATK, DEF, mitigation, and crit rate beside the portrait, mirroring the same order for party and foes. HoT/DoT markers appear beneath each portrait, collapsing duplicate effects into a single icon that shows a small stack count. Shared fallback art appears when portraits are missing, and the layout scales down on small screens so both the bars and numeric values remain readable.

Snapshots from the backend are polled once per frame-rate tick rather than on a
fixed interval. Each request dispatches events with the round-trip time so
`GameViewport` can log performance and show a stained-glass status panel with a
spinner while updates are in flight. Incoming party and foe arrays are compared
to the previous snapshot to avoid unnecessary re-renders.

## Testing
- `bun test frontend/tests/battleview.test.js`

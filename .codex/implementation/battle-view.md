# Battle View

`BattleView.svelte` renders turn-based encounters inside `MenuPanel`. It draws a
random backdrop from the shared `assetLoader` and displays the party and foes in
opposing columns. Portraits are now 6 rem square for better visibility and sit
beneath Pokémon-style HP bars that track current health.

Each combatant lists key stats beside the portrait, including ATK, DEF,
mitigation, and crit rate. The layout scales down on small screens so both the
bars and numeric values remain readable.

Snapshots from the backend are polled dynamically rather than on a fixed
interval. Each request dispatches events with the round-trip time so
`GameViewport` can log performance and show a stained-glass status panel with a
spinner while updates are in flight.

## Testing
- `bun test frontend/tests/battleview.test.js`

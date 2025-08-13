# Map Display

`MapDisplay.svelte` replaces the old `RunMap` and wraps the run's floor layout
in `MenuPanel`. Each room is rendered as a stained-glass button with a
`lucide-svelte` icon matching its type (battle, rest, shop, boss, or unknown).
The component emits a `select` event when the player chooses a room.

## Testing
- `bun test frontend/tests/mapdisplay.test.js`

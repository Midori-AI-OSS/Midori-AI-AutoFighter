# Room View

`RoomView.svelte` displays the outcome of a room interaction. Foes are
rendered along the top row with simple health bars while party members
appear on the bottom row with small circles representing ultimate meters.
The view stretches to fill the viewport so desktop and tablet screens can
show up to ten foes, while phones display only the first three foes and
hide the rest.

## Testing
- `bun test frontend/tests/api.test.js`

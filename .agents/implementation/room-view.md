# Room View

`RoomView.svelte` displays the outcome of a room interaction. Foes are
rendered along the top row with simple health bars while party members
appear on the bottom row with small circles representing ultimate meters.
The view stretches to fill the viewport so desktop and tablet screens can
show up to ten foes, while phones display only the first three foes and
hide the rest.

Progress snapshots expose `active_id`, and `RoomView.svelte` uses it to
overlay a small arrow above the acting party member or below the acting
foe. The arrow bounces to draw attention but respects the user's
`prefers-reduced-motion` setting by disabling the animation when motion is
reduced.

## Testing
- `bun test frontend/tests/api.test.js`

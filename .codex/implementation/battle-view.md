# Battle View

`BattleView.svelte` is a placeholder combat screen rendered inside `MenuPanel`.
It now draws a random backdrop from the shared `assetLoader` and overlays a row
of party portraits tinted by their damage types. Icons reuse
`getCharacterImage`, and borders pull colors via `getElementColor` to match the
party picker. The component reserves space for timelines and actions while
backend integration is still pending.

## Testing
- `bun test frontend/tests/battleview.test.js`

# Rest Room Menu

`RestRoom.svelte` presents **Pull Character**, **Switch Party**, **Craft**, and
**Leave** buttons within `MenuPanel`. Selecting **Craft** shows `CraftingMenu`,
which fetches item counts and posts to `/gacha/craft` and `/gacha/auto-craft`.
Choosing **Leave** advances the run via `advanceRoom` and immediately loads the
next map node.

## Testing
- `bun test`

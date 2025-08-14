# Rest Room Menu

`RestRoom.svelte` presents **Pull Character**, **Switch Party**, **Craft**, and
**Leave** buttons within `MenuPanel`. Selecting **Craft** shows `CraftingMenu`,
which fetches item counts and posts to `/gacha/craft` and `/gacha/auto-craft`.

## Testing
- `bun test`

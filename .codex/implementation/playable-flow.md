# Playable Web Flow

The Svelte frontend starts a run by calling the Quart backend's `/run/start`
endpoint with the selected party. The backend creates a run in the encrypted
`save.db` (path set by `AF_DB_PATH` and key from `AF_DB_KEY` or
`AF_DB_PASSWORD`) and returns a `run_id` with the initial map layout.

After confirming the lineup in a modal PartyPicker, players can reopen the map
at any time via the **Map** button, which fetches the latest floor state and
renders nodes in `MapDisplay.svelte`. The **Edit** button loads the player's
configuration and opens `PlayerEditor` so pronouns, damage type, and starting
stats can be adjusted outside a run. The **Pulls** menu opens a gacha panel that
shares pity and upgrade-item currency with rest-node pulls. The **Craft** menu
lists upgrade items, calls `/gacha/craft` to convert materials, and toggles
auto-crafting. Selecting a room triggers the matching endpoint
(`/rooms/{run_id}/battle`, `/shop`, or `/rest`) and the map refreshes from the
backend to reflect progress.

This minimal loop lets the web build start a run, navigate the floor, and
trigger room logic while persisting state between HTTP calls and sessions.

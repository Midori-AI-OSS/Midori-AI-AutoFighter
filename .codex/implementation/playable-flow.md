# Playable Web Flow

The Svelte frontend starts a run by calling the Quart backend's `/run/start`
endpoint. The backend creates a run in the encrypted `save.db` (path set by
`AF_DB_PATH` and key from `AF_DB_KEY` or `AF_DB_PASSWORD`) with a generated
map and returns a `run_id` along with the map layout.

After the player confirms their lineup in a modal PartyPicker, the frontend
sends the chosen party to `/party/{run_id}` and displays the map using
`MapDisplay.svelte`, which renders each node as a stained-glass button with a
lucide icon. Each request reads and writes run state from the encrypted
database, allowing progress to persist between HTTP calls and sessions.

This minimal loop lets the web build start a run, save party selection, and
retrieve the map for navigation.

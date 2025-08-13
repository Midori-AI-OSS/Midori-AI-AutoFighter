# Room Endpoints

The Quart backend exposes routes for core gameplay rooms. Each accepts the
current `run_id` and returns data generated from the plugin system and seeded
maps.

## Routes

- `GET /players` – lists all plugin player characters with fields:
  - `id`: plugin identifier
  - `name`: display name
  - `owned`: whether the player owns this character
  - `is_player`: true for the player's avatar
- `POST /run/start` – seeds a `MapGenerator` with the run ID and stores a 45
  node map; responses include the full map and a `current` pointer.
- `GET /rooms/images` – returns a mapping of room types to background image URLs
  served from `/assets/...`.
- `GET /assets/<path>` – serves static assets bundled under `backend/assets/`.
- `POST /rooms/<run_id>/battle` – validates the next map node is a battle,
  spawns a random player plugin not in the party as the foe, scales all stats by
  floor, room index, loop, and Pressure, triggers passives, exchanges attacks with
  the party, and advances the map pointer. Responses include full stats for both
  sides.
- `POST /rooms/<run_id>/shop` – validates the next node is a shop, deducts the
  provided `cost` from the party's shared gold pool and, when an `item` is
  supplied, appends it to the first member's item list.
- `POST /rooms/<run_id>/rest` – validates the next node is a rest room, heals
  the party to full, and advances the map pointer.
- `POST /rooms/<run_id>/boss` – validates the next node is a `battle-boss-floor`
  room and runs a high-powered battle before advancing the map pointer. Responses
  include full stats for party and foe.

All routes read and write state through `SaveManager`, which uses `AF_DB_PATH`
and a key from `AF_DB_KEY` or `AF_DB_PASSWORD`.

## Testing
- `uv run pytest backend/tests/test_app.py::test_players_and_rooms`
- `uv run pytest backend/tests/test_app.py::test_room_images`
- `uv run pytest backend/tests/test_mapgen.py::test_generator_deterministic`
- `uv run pytest backend/tests/test_passives.py`

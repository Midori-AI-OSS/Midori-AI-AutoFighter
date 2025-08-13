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
  node map; responses include the full map and a `current` pointer. Each floor
  guarantees at least one rest room appears after the first shop.
- `GET /rooms/images` – returns a mapping of room types to background image URLs
  served from `/assets/...`.
- `GET /player/stats` – returns grouped stats and status lists for the player's avatar along with a clamped `refresh_rate` value.
- `GET /assets/<path>` – serves static assets bundled under `backend/assets/`.
- `POST /rooms/<run_id>/battle` – validates the next map node is a battle,
  spawns a random player plugin not in the party as the foe, scales all stats by
  floor, room index, loop, and Pressure, triggers passives, exchanges attacks with
  the party, and advances the map pointer. Responses include full stats for both
  sides plus up to three unused `card_choices` of the appropriate star rank and the
  party's full `cards` list.
- `POST /rooms/<run_id>/shop` – validates the next node is a shop, heals the
  party by 5% of its total max HP, deducts the provided `cost` from the shared
  gold pool, and appends any purchased `item` to a shared relic list. Responses
  include updated `gold`, `relics`, and `cards` values.
- `POST /rooms/<run_id>/rest` – validates the next node is a rest room, allows
  gacha pulls or party swaps, and advances the map pointer. Responses include the
  current `cards` inventory.
- `POST /rooms/<run_id>/boss` – validates the next node is a `battle-boss-floor`
  room and runs a high-powered battle before advancing the map pointer. Responses
  mirror normal battles but scale foe stats heavily and offer higher-star
  `card_choices` when available.
- `POST /cards/<run_id>` – accepts a chosen `card` ID from the latest battle and
  adds it to the party if unowned, returning the updated `cards` list.

All routes read and write state through `SaveManager`, which uses `AF_DB_PATH`
and a key from `AF_DB_KEY` or `AF_DB_PASSWORD`. Party data stored per run
includes member IDs, shared gold, and relics.

## Testing
- `uv run pytest backend/tests/test_app.py::test_players_and_rooms`
- `uv run pytest backend/tests/test_app.py::test_room_images`
- `uv run pytest backend/tests/test_mapgen.py::test_generator_deterministic`
- `uv run pytest backend/tests/test_passives.py`

# Backend

Quart game logic server listening on port `59002`. A `SaveManager` wrapper
handles SQLCipher encryption and reads the save database at
`backend/save.db` by default. Set `AF_DB_PATH` to change the location and
provide either `AF_DB_KEY` or `AF_DB_PASSWORD` for encryption.

## Setup

```bash
cd backend
uv sync
uv run app.py
```

The root endpoint returns a simple status payload. Additional routes support
starting runs with a seeded 45-room map, updating the party, retrieving floor
maps, listing available player characters, returning room background images,
editing player pronouns and starting stats, and posting actions to battle, shop,
rest, or floor boss rooms. Room endpoints no longer advance the map
automatically—after processing a room (and any card rewards) the frontend must
call `POST /run/<run_id>/next` to move to the next node. `POST /run/start`
accepts a JSON body with `party` (1–5 owned character IDs including `player`)
and an optional `damage_type` for the player chosen from Light, Dark, Wind,
Lightning, Fire, or Ice. The response includes the validated party with passive
names. Run state is stored through the `SaveManager` in `backend/save.db` by
default; `compose.yaml` bind-mounts the `backend/` directory so the database is
persisted on the host.

`GET /gacha` returns the current pity counter, element-based upgrade items,
owned characters with their duplicate stacks, and whether auto-crafting is
enabled. `POST /gacha/pull` performs 1, 5, or 10 pulls, awarding 5★ or 6★
characters or 1★–4★ upgrade items keyed by element. Higher pity increases the
chance of rarer items on failed pulls. Automatic crafting of upgrade items is
disabled by default but can be toggled with `POST /gacha/auto-craft`, which
converts 125 lower-star items into one higher star and ten 4★ items into a
ticket.

`GET /player/editor` returns saved pronouns, element, and stat allocations for
the player. `PUT /player/editor` validates pronouns up to 15 characters,
ensures the chosen damage type is Light, Dark, Wind, Lightning, Fire, or Ice,
and rejects edits if a run is active or if allocations exceed the available
points. Each point boosts the matching stat by 1% (100 points doubles it).

Static assets are served from `/assets/<path>`; for example, `GET /rooms/images`
returns a JSON mapping of room types to background image URLs under `/assets/...`.

## Docker

`Dockerfile.python` installs uv, Docker, and Docker Compose in separate steps and prepares the `/.venv` directory with individual RUN commands. It exposes a `UV_EXTRA` build argument for optional extras.

```bash
docker build -f Dockerfile.python --build-arg UV_EXTRA="llm-cpu" -t autofighter-backend .
```

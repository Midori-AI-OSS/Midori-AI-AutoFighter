# Midori AI AutoFighter

Midori AI AutoFighter is being rebuilt as a web application. A Svelte frontend
communicates with a Python Quart backend, and Docker Compose orchestrates both
services. The legacy Pygame prototype lives in `legacy/` and remains untouched.

## Directory Structure

```
frontend/   # Svelte frontend
backend/    # Quart backend and game logic
legacy/     # Previous Pygame version (read-only)
```

## Setup

1. Install [uv](https://github.com/astral-sh/uv) and
   [bun](https://bun.sh/).
2. Start both services with Docker Compose (bind-mounted source):

```bash
docker compose up --build frontend backend
```

Compose bind-mounts `frontend/` and `backend/` into the containers. The backend
stores its database at `backend/save.db` by default (override with
`AF_DB_PATH`). Provide `AF_DB_KEY` or `AF_DB_PASSWORD` for encryption via the
`SaveManager`. The Svelte dev server listens on `59001` and the Quart backend
on `59002`.

### Dev Workflow
- Code changes are reflected immediately since source is bind-mounted into the containers.
- Frontend entrypoint runs `bun install` if `node_modules/` is missing, then starts the dev server.
- Backend entrypoint runs `uv sync` (respects `UV_EXTRA`) and launches the Quart app with `uv run app.py`.
- The backend serves static assets under `/assets/*` and exposes `GET /rooms/images` with room background URLs.

### Optional LLM Dependencies

Install extras to experiment with local language models. Each extra bundles
LangChain, Transformers, and a matching PyTorch build:

```bash
uv sync --extra llm-cuda  # NVIDIA GPUs (CUDA drivers required)
uv sync --extra llm-amd   # AMD/Intel GPUs (ROCm or oneAPI)
uv sync --extra llm-cpu   # CPU-only
```

Selecting the correct extra ensures hardware acceleration when available. These
packages are optional; the core game runs without them.

3. Run the backend directly (without Docker):

```bash
cd backend
uv run app.py
```

The server uses `AF_DB_PATH` for the save database (default
`backend/save.db`). Supply `AF_DB_KEY` or `AF_DB_PASSWORD` to open the
encrypted database; without either it opens plaintext.

4. Install the latest build into another project:

```bash
uv add git+https://github.com/Midori-AI/Midori-AI-AutoFighter@main
```

### Docker Compose LLM Profiles

Enable optional LLM dependencies with Compose profiles. All profiles reuse port
`59002` and intentionally conflict with the standard backend—only one profile
should run at a time:

```bash
docker compose --profile llm-cuda up --build   # backend on 59002
docker compose --profile llm-amd up --build    # backend on 59002
docker compose --profile llm-cpu up --build    # backend on 59002
```

## Responsive Layout

The Svelte frontend targets three breakpoints:

- **Desktop** – displays the party picker, player editor, and floor map around
  the active menu so most information is visible at once.
- **Tablet** – shows two panels side by side when space permits.
- **Phone** – focuses on a single menu at a time for clarity on small screens.

The interface adapts automatically based on viewport width.

## Publishing

Docker images for both services will be published to Docker Hub. Native
dependencies are handled inside the images, so no manual wheel management is
required.

## Testing

Run the test suite before submitting changes:

```bash
cd backend
uv run pytest
```

## Plugins

The game auto-discovers classes under `plugins/` and `mods/` by `plugin_type`
and wires them to a shared event bus. See
`.codex/implementation/plugin-system.md` for loader details and examples.

## Player Creator

Use the in-game editor to pick a body and hair style, choose a hair color and
accessory, and distribute 100 stat points. Spending 100 of each damage type's
4★ upgrade items grants one extra stat point. The result is stored in the
encrypted `save.db` database for new runs.

## Stat Screen

View grouped stats and status effects. The display refreshes every few frames
and supports plugin-provided lines. Categories cover core, offense, defense,
vitality, advanced data, and status lists for passives, DoTs, HoTs, damage types,
and relics. When **Pause on Stat Screen** is enabled in Options, opening the
screen halts gameplay until closed.

## Damage and Healing Effects

DoT and HoT plugins manage ongoing damage or recovery. Supported DoTs include
Bleed, Celestial Atrophy, Abyssal Corruption (spreads on death), Blazing
Torment (extra tick on action), Cold Wound (five-stack cap), and Impact Echo
(half of the last hit each turn). HoTs cover Regeneration, Player Echo, and
Player Heal.

## Battle Room

Start a run in a battle scene that renders placeholder models, triggers party
passives, and runs event-driven stat-based attacks against a `Slime` scaled by
floor, room, Pressure level, and loop count. Foes inherit from a dedicated
`FoeBase` that mirrors player stats; the default `Slime` reduces them by 90%
on spawn. The scene shows floating damage numbers and status icons and flashes
red and blue with an Enraged buff after 100 turns (500 for floor bosses).

## Rest Room

Recover HP or trade upgrade stones for a +5 Max HP boost. Each floor permits one
rest, and map generation ensures at least two rest rooms per floor. The scene
displays a brief message after the action.

## Shop Room

Buy upgrade items or cards with star ratings. Inventory scales by floor,
purchases add items to your inventory and disable the button, class-level
tracking guarantees at least two shops per floor, and gold can reroll the
current stock.

## Event and Chat Rooms

Event Rooms offer text-based encounters with selectable options that use seeded
randomness to modify stats or inventory. Chat Rooms, available only when the LLM
profiles are installed, let players send a single message to an LLM character,
track usage per floor, and do not count toward the floor's room limit; only six
chats may occur on each floor.

## Map Generation

New runs begin by selecting up to four owned allies in a party picker before the
map appears. Runs then progress through 45-room floors built by a seeded
`MapGenerator`. Each floor includes at least two shops and two rest rooms,
battle nodes marked as `battle-weak` or `battle-normal`, and ends in a
`battle-boss-floor`. Chat scenes may appear after battles only when the LLM
profiles are installed and do not affect room count.

## Playable Characters

The roster in `plugins/players/` currently includes and each entry lists its
`CharacterType`. All players start with 1000 HP, 100 attack, 50 defense, a 5%
crit rate, 2× crit damage, 1% effect hit rate, 100 mitigation, 0 dodge, and 1
in all other stats. Listed damage types use the classic naming from the
Pygame version:

- Ally (B, random damage type)
- Becca (B, random damage type)
- Bubbles (A, random damage type)
- Carly (B, Light)
- Chibi (A, random damage type)
- Graygray (B, random damage type)
- Hilander (A, random damage type)
- Kboshi (A, random damage type)
- Lady Darkness (B, Dark)
- Lady Echo (B, Lightning)
- Lady Fire and Ice (B, Fire or Ice)
- Lady Light (B, Light)
- Lady of Fire (B, Fire)
- Luna (B, Generic)
- Mezzy (B, random damage type)
- Mimic (C, random damage type)
- Player (C, chosen damage type)

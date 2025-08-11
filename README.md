# Midori AI AutoFighter

This repository is the starting point for a Panda3D-based rewrite of Midori AI AutoFighter.
The previous Pygame codebase lives in `legacy/` and must remain unmodified.

## Directory Structure

```
assets/
  audio/
  models/
  textures/
game/
  actors/
  ui/
  rooms/
  gacha/
  saves/
plugins/
mods/
llms/
legacy/
```

## Setup

1. Install [uv](https://github.com/astral-sh/uv).
2. Install dependencies:

   ```bash
   uv sync
   ```

   Panda3D ships prebuilt wheels.

### Optional LLM Dependencies

Install extras to experiment with local language models. Each extra bundles
LangChain, Transformers, and a matching PyTorch build.

```bash
uv sync --extra llm-cuda  # NVIDIA GPUs (CUDA drivers required)
uv sync --extra llm-amd   # AMD/Intel GPUs (ROCm or oneAPI)
uv sync --extra llm-cpu   # CPU-only
```

Selecting the correct extra ensures hardware acceleration when available. These
packages are optional; the core game runs without them.

3. Run the game:

   ```bash
   uv run main.py
   ```

4. Install the latest build into another project:

   ```bash
   uv add git+https://github.com/Midori-AI/Midori-AI-AutoFighter@main
   ```

## Publishing

The package will be published to PyPI as `autofighter`. Panda3D provides platform-specific
wheels, so native dependencies must be considered when distributing builds.

## Testing

Run the test suite before submitting changes:

```bash
uv run pytest
```

## Plugins

The game auto-discovers classes under `plugins/` and `mods/` by `plugin_type` and wires them to a shared event bus. See `.codex/implementation/plugin-system.md` for loader details and examples.

## Player Creator

Use the in-game editor to pick a body and hair style, choose a hair color and accessory, and distribute 100 stat points. Spending 100 of each damage type's 4★ upgrade items grants one extra stat point. The result is saved to `player.json` for new runs.

## Stat Screen

View grouped stats and status effects. The display refreshes every few frames and supports plugin-provided lines. Categories cover core, offense, defense, vitality, advanced data, and status lists for passives, DoTs, HoTs, damage types, and relics. When **Pause on Stat Screen** is enabled in Options, opening the screen halts gameplay until closed.

## Damage and Healing Effects

DoT and HoT plugins manage ongoing damage or recovery. Supported DoTs include Bleed, Celestial Atrophy, Abyssal Corruption (spreads on death), Blazing Torment (extra tick on action), Cold Wound (five-stack cap), and Impact Echo (half of the last hit each turn). HoTs cover Regeneration, Player Echo, and Player Heal.

## Battle Room

Start a run in a battle scene that renders placeholder models, runs messenger-driven stat-based attacks, scales foes by floor, room, Pressure level, and loop count, shows floating damage numbers and attack effects, adds status icons, and flashes the room red and blue with an Enraged buff after 100 turns (500 for floor bosses).

## Rest Room

Recover HP or trade upgrade stones for a +5 Max HP boost. Each floor permits one rest, and map generation ensures at least two rest rooms per floor. The scene displays a brief message after the action.

## Shop Room

Buy upgrade items or cards with star ratings. Inventory scales by floor, purchases add items to your inventory and disable the button, class-level tracking guarantees at least two shops per floor, and gold can reroll the current stock.

## Event and Chat Rooms

Event Rooms offer text-based encounters with selectable options that use seeded randomness to modify stats or inventory. Chat Rooms let players send a single message to an LLM character, track usage per floor, and do not count toward the floor's room limit; only six chats may occur on each floor.

## Map Generation

New runs begin by selecting up to four owned allies in a party picker before the map appears. Runs then progress through 45-room floors built by a seeded `MapGenerator`. Each floor includes at least two shops and two rest rooms, always ends in a floor boss, and can add extra rooms or boss fights as Pressure Level rises. Battle rooms may spawn chat rooms after combat without affecting room count.

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

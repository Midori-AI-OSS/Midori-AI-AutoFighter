# Midori AI AutoFighter

This repository is the starting point for a Panda3D-based rewrite of Midori AI AutoFighter.
The previous Pygame codebase lives in `legacy/` and must remain unmodified.

## Directory Structure

```
assets/
  audio/
  models/
  textures/
plugins/
mods/
llms/
legacy/
```

## Setup

1. Install [uv](https://github.com/astral-sh/uv).
2. Run the game:

   ```bash
   uv run main.py
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

Custom modules live in `plugins/` or `mods/`. See `.codex/instructions/plugin-system.md` for details on creating new plugins.

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

Runs progress through 45-room floors built by a seeded `MapGenerator`. Each floor includes at least two shops and two rest rooms, always ends in a floor boss, and can add extra rooms or boss fights as Pressure Level rises. Battle rooms may spawn chat rooms after combat without affecting room count.

## Playable Characters

The roster in `plugins/players/` currently includes:

- Ally
- Becca
- Bubbles
- Carly
- Chibi
- Graygray
- Hilander
- Kboshi
- Lady Darkness
- Lady Echo
- Lady Fire and Ice
- Lady Light
- Lady of Fire
- Luna
- Mezzy
- Mimic

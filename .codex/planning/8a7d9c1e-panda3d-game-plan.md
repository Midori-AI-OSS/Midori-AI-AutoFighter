# Panda3D Game Remake Planning

## Goal
Fully remake the Pygame-based roguelike autofighter in Panda3D with 3D-ready architecture while retaining plugin-driven combat, menus, stat screens, and a multi-room run map.

## 1. Project Setup
1. Move current Pygame code into `legacy/`.
2. Run `uv init` to create a fresh environment.
3. Install Panda3D with `uv add panda3d`; optional LLM extras via `uv add --optional llm`.
   - Include LLM tooling such as `langchain` and Hugging Face `transformers`.
   - Use prebuilt Panda3D wheels; focus build notes on LangChain/transformers for NVIDIA, Intel/AMD GPU, and CPU-only setups.
4. Add `main.py` launching `ShowBase` and rendering a placeholder cube to verify the engine.
5. Scaffold `assets/` (`models/`, `textures/`, `audio/`), `plugins/`, `mods/`, and user-managed `llms/` directories and document the structure in `README.md`.
6. Update `README.md` to warn contributors not to modify `legacy/` and show how to install the latest code via `uv add git+https://github.com/Midori-AI/Midori-AI-AutoFighter@main`.
7. Commit minimal setup once `main.py` runs.
8. Define a `pyproject.toml` package named `autofighter` and expose an entry point for `main.py`.
   - Research publishing `autofighter` to PyPI once stable; expect moderate effort due to native dependencies and asset management.

## 2. Core Architecture
1. Implement a new `ShowBase` subclass from scratch and exclude legacy imports.
2. Convert event logic to Panda3D's `messenger` and `taskMgr` while keeping frame loops light for low-end hardware.
3. Replace Pygame rendering with Panda3D node graphs.
4. Rebuild the plugin loader and APIs so new player, weapon, passive, DoT, and HoT plugins mirror current concepts without reusing legacy code and expose a mod interface.
5. Add a scene manager capable of swapping menus, gameplay states, and overlays.
6. Organize source under a `game/` package with submodules (`actors/`, `ui/`, `rooms/`, `gacha/`, `saves/`).
7. Define a `Stats` dataclass holding core attributes; share between players and foes.
8. Provide an event bus wrapper for `messenger` so plugins can subscribe and emit without engine imports.

## 3. UI Foundation
1. **Theme: dark, glassy visuals**
   - Background: blurred gradients in deep blues/purples with rounded, glass-like edges.
   - Panels: colored borders matching mood with subtle shadows.
   - Headers: bold titles, small icons (close "X", status dots), accent highlights.
   - Text: modern sans-serif in light gray or white.
   - Buttons: rounded pills with gradients or solid accents; hover slightly scales and brightens.
   - Inputs: rounded fields with faint borders and blurred backgrounds.
2. **Menus**
   - Build main menu with *New Run*, *Load Run*, *Edit Player*, *Options*, *Quit*.
   - Option stubs:
     - *New Run* starts a fresh state.
     - *Load Run* lists save slots.
     - *Edit Player* opens customization.
       - Offer three body types and selectable hair styles, colors, and accessories.
       - Present a 100-point stat pool; each point grants +1% to a chosen stat.
       - Spending 100 of each damage type's 4★ upgrade items buys one extra point.
   - Use DirectGUI and ensure keyboard/mouse navigation.
3. **Options submenu**
   - Sound-effects volume.
   - Music volume.
   - Toggle stat-screen pause behaviour.
4. Code structure:
   - Create a `ui/` package with modules for menus, options, and widgets.
   - Use a base `MenuScreen` class that handles navigation and animation hooks.

## 4. Player Stat Screen
1. Overlay displays and groups data:
   - **Core stats:** HP, Max HP (MHP), EXP, Level, EXP buff multiplier, Actions per Turn.
   - **Offense:** Attack, Crit Rate, Crit Damage, Effect Hit Rate, base damage type.
   - **Defense:** Defense, Mitigation, Regain, Dodge Odds, Effect Resistance.
   - **Vitality:** boosts EXP gain and all other stats; lowers damage taken down to a minimum of 1 and buffs damage dealt, healing, and DoT damage; shown separately because it influences both offense and defense.
   - **Advanced:** Action Points, Actions per Turn, cumulative Damage Taken/Dealt, and Kills.
   - **Status:**
     - *Passives:* list all active entries from `plugins/passives`.
    - *DoTs:*
       - `Bleed` – physical wounds that bypass mitigation and deal 2% Max HP per turn.
       - `Celestial Atrophy` – light damage that also lowers the target's Attack each tick.
       - `Abyssal Corruption` – dark damage that spreads to nearby foes when the target falls.
       - `Abyssal Weakness` – dark damage that reduces Defense while active.
       - `Gale Erosion` – wind damage stripping 1% Mitigation per tick.
       - `Charged Decay` – lightning damage with a 10% stun chance on the final tick.
       - `Frozen Wound` – ice damage that slows action speed by 5% each turn.
       - `Blazing Torment` – fire damage that inflicts an extra tick whenever the target acts.
       - `Cold Wound` – mild ice damage that stacks up to five times.
       - `Twilight Decay` – light/dark damage draining 0.5% Vitality per turn.
       - `Impact Echo` – physical shockwaves repeating 50% of the last hit for three turns.
       - DoTs stack indefinitely unless a specific effect lists a cap (only `Cold Wound` has a five-stack limit).
       - All DoT-induced stat changes are cleared after each fight unless a card explicitly makes them permanent.
     - *HoTs:*
       - `Regeneration` – heals a flat amount (5 HP) each turn for three turns.
       - `PlayerName's Echo` – when a generic-type ally deals damage, party members heal for 20% of that damage over five turns.
       - `PlayerName's Heal` – certain themed allies give wounded teammates an instant heal plus 1% Max HP per turn for five turns.
       - HoTs have no stack cap and, like DoTs, expire when the battle ends unless a card states otherwise.
     - *Damage types:*
       - `Generic`
       - `Light`
       - `Dark`
       - `Wind`
       - `Lightning`
       - `Fire`
       - `Ice`
     - *Relics:* show collected stacks by name and star rank.
   - Track stats using Python's arbitrary-precision integers; chunk internally only if performance demands it and display formatted single values to players.
2. Bind fields to player data and refresh at a user-defined rate (default every 5 frames, adjustable from every frame to every 10 frames).
3. ESC or close returns to the previous scene and respects the Options pause setting.
4. Code structure:
   - Create `StatPanel` widgets for each category and populate from a shared `Stats` dataclass.
   - Expose hooks so plugins can append custom lines to the Status section.

## 5. Map and Room Types
1. Room categories: rest, chat, battle-weak, battle-normal, battle-boss, **battle-boss-floor**, shop.
   - Each floor has at least two shops and two rest stops.
   - Chats occur after fights without consuming room count.
   - Chat rooms let players RP with an LLM copy of a character that offers one-message tips or comments about the run.
   - Players may send only one message per chat room, capped at six chats per floor.
2. Map generator: 45-room floors for ~100 floors; endless looping after final floor.
   - Optional **Pressure Level** boosts foe stats by +5%–10% per tier and is selectable up to the highest level cleared.
   - Display Pressure Level next to foe names in combat, e.g., `Luna (5)`.
   - Every 5 Pressure levels add an extra foe per battle room up to 10; once capped, loot drops decrease.
   - Every 10 Pressure levels add one more room per floor before the boss.
   - Every 20 Pressure levels insert additional back-to-back boss rooms.
   - Enemy stats scale as base stats × floor level × room level × loop count.
   - Each loop multiplies enemy stats by 1.2× ±5% and, after the second loop, grants +1 Pressure level for future runs.
   - Battle rooms scale foes by 1.05× ±5% per fight.
3. Final room each floor is **battle-boss-floor** with a single foe at 100× floor level × room level × loop count.
4. Display: color-coded nodes, readable icons, highlight current location, show valid paths.
5. Transitions load correct room scenes using shared templates with floor-specific themes.
6. Starting around room 20, gradually shift floor visuals toward the upcoming boss room (e.g., Luna’s floor gains more night and star motifs) so players can sense the next encounter.
7. Combat accuracy driven solely by stats; reusable, recolorable effects for attack types and team buffs.
8. Fights that exceed 100 turns (500 for floor bosses) trigger a slow red/blue flash on the room to warn of drawn-out battles.
   - Each turn after the flash begins grants foes a +40% Attack `Enraged` buff.
9. Rewards:
   - Normal fights: 5% chance to drop a relic (98% of which are 1★), grant gold = 5 × (loop number × random float 1.01–1.25), drop 1–2★ upgrade items scaled by floor/room/Pressure, and award a 1–2★ card.
   - Bosses: 25% chance to drop a relic with 1–5★ ranks, grant extra gold = 20 × (loop number × random float 1.53–2.25), drop 1–3★ upgrade items scaled by difficulty, and award a 1–5★ card.
   - Floor bosses: guaranteed relic drops (3★ at 98% odds), largest gold bonus = 200 × (loop number × random float 2.05–4.25), drop 3–4★ upgrade items scaled by difficulty, award 3–5★ cards, and grant pull tickets that scale with Pressure/loop up to 5 per floor boss.
   - Relics come in 1–5★ ranks using the shared star-color scheme; stacks have no cap and drop tables favor relics the player lacks.
   - Cards are unique collectibles with one copy each; design ~100 cards per combat theme (DoT, melee, etc.), with 1★ effects providing minor perks (e.g., heal 1% when dealing DoT) and 5★ effects offering major boons (e.g., temporary ally joins the party).
10. Code structure:
    - Create a `MapNode` dataclass storing room type, links, and reward data.
    - Implement `Room` subclasses (`RestRoom`, `BattleRoom`, `ChatRoom`, etc.) with shared interfaces for entry, reward, and exit hooks.
    - Build a `chat/` module that routes one-shot messages to local or remote LLMs stored under `llms/`.
    - Seed each floor from a run-specific base seed, mutate it several times, and forbid seed reuse so players cannot reproduce identical maps.

## 6. Gacha Character Recruitment
1. Between runs, players spend collected upgrade items on gacha pulls for recruitable characters and chatable allies.
   - Seed the pool with existing player plugins such as Ally, Becca, Bubbles, Carly, Chibi, Graygray, Hilander, Kboshi, Lady Darkness, Lady Echo, Lady Fire and Ice, Lady Light, Luna, Mezzy, and Mimic.
2. Pull options: spend for 1, 5, or 10 pulls.
   - Play a pre-made video keyed to the highest rarity obtained (1★–6★); videos are skippable or fast-forwardable.
   - Base odds heavily favor ≥2★ rewards (~99%), with 5★ and 6★ odds rising as pity grows.
   - After the video, display a menu listing all items/characters from the pull batch.
3. Pity system: odds start at 0.001%, rise slowly, ~5% at pull 159, guaranteed featured character at pull 180; counter resets on success. After owning all 5★ characters, soft pity for 6★ increases by 1000 pulls per 6★ owned with a hard cap at 2000.
4. Duplicate logic:
   - Before completing the 5★ roster: 25% chance to pull a duplicate, 75% new 5★.
   - After collecting all 5★ characters: 25% chance to get a duplicate of a heavily stacked 5★, 75% chance for a 5★ with few stacks; 6★ rolls remain extremely rare.
5. Vitality bonus: first duplicate adds 0.01%; each additional stack adds 5% more than the previous increment (0.01%, 0.0105%, 0.011025%, ...). Vitality increases EXP gain and all other stats.
6. Failed pulls give upgrade items (1★–4★) matching damage types; dual-type characters require both types.
   - Costs: 1000×1★, 500×2★, 100×3★, or 20×4★ items per upgrade level.
   - 125 lower-star items combine into one higher star.
   - Trading 10×4★ items grants one additional pull.
   - Infusing a character outside runs lets players pick which stat to boost: 45×4★ items per tier for normal stats, 180×4★ for Vitality or similar power stats.
7. 6★ characters are dual damage types (e.g., Lady Fire and Ice, Persona Light and Dark) and are far rarer than 5★; even at full pity they appear only ~0.01% of the time.
8. Star colors are shared across all systems: 1★ gray, 2★ blue, 3★ green, 4★ purple, 5★ red, 6★ gold.
9. Provide crafting menus for converting items to higher stars or extra pulls.
10. Code structure:
    - Implement a `GachaManager` handling pity counts, roll tables, and reward serialization.
    - Define `UpgradeItem` and `Character` dataclasses to represent inventory pieces and recruitable units.
    - Store upgrade items and character stacks in the encrypted save database for cross-run persistence.

## 7. Encrypted Save System
1. Store run and player data in SQLite secured with SQLCipher.
2. Minimize I/O via batched writes and compact schemas; supply migration tooling for legacy saves.
3. Derive SQLCipher keys from a user-supplied salted password stored in encrypted config with optional cloud backup.
4. Consider alternative key sources (OS keyrings, env vars, hardware tokens) for advanced setups.
5. Code structure:
   - Wrap database access in a `SaveManager` module with context-managed sessions.
   - Provide schema migrations using simple versioned scripts to keep saves forward compatible.

## 8. Asset Pipeline
1. Research art styles: low-poly look reminiscent of *Final Fantasy VII* and *VIII* or pixelated 3D hybrids.
2. Evaluate free/CC model sources for Panda3D compatibility.
3. Establish conversion workflow (e.g., Blender → `.bam`/`.egg`) with cached builds.
4. Create asset loading utilities and preload to reduce runtime stalls.
5. Code structure:
   - Maintain an `assets.toml` manifest mapping asset keys to file paths and hashes.
   - Build an `AssetManager` that loads and caches models, textures, and sounds on demand.

## 9. Testing and Iteration
1. Unit tests for menus, stat screen, map navigation, gacha logic, and data wiring.
2. Run `uv run pytest` after each major change.
3. Review and update build scripts for Windows, Linux, and Android:
   - Audit `builder/` scripts per OS.
   - Verify Panda3D and dependency bundling.
   - Perform smoke builds for cross-platform checks.
4. Add a **Give Feedback** menu button that opens a pre-filled GitHub issue.
5. Update `.codex/planning` with follow-up tasks as features stabilize.
6. Code structure:
   - Configure pytest fixtures for headless Panda3D contexts.
   - Add CI workflow steps to run tests and lint on pushes and pull requests.

## Open Questions
- Where should DoT, passive, and damage-type info appear on the stat screen for best readability? Separate tabs or a scrollable list?
- How should we balance 5★ rates against extremely rare 6★ dual-type characters and set pity thresholds?
- What UX should crafting menus use to convert upgrade items or trade them for pulls?
- Which additional options should testers tweak for stat-screen pause behaviour, game speed, or accessibility?
- How should key backups be handled across platforms for the salted-password save encryption?
- Should **Pressure Level** remain the final name for the difficulty slider, and is showing it as `Name (5)` over foe heads clear enough to distinguish it from room-based enrages?
- Do the proposed star colors (1 gray, 2 blue, 3 green, 4 purple, 5 red, 6 gold) read well across UI elements and loot types? This needs playtesting once the UI exists.
- What flash rate and intensity keep the red/blue overtime warning noticeable without causing discomfort? Allow users to adjust color, speed, or disable it entirely.

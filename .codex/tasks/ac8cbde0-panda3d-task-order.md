# Panda3D Remake Task Order

## Summary
Define the execution order for Panda3D remake subtasks based on the existing task list and planning document.
Review `.codex/planning/8a7d9c1e-panda3d-game-plan.md` before starting or auditing any step.

Coders must check in with the reviewer or task master before marking tasks complete.

> **Task Master Reminder:** Keep `myunderstanding.md` describing the game's flow up to date.

## Tasks
* [x] Menu scaling and layout responsiveness (`b9e25489`) – implement global DirectGUI scaling so menus keep a consistent size across window dimensions and follow the requested layout.
   - [x] Create a scaling helper anchored to a base resolution.
   - [x] Apply scaling to all menus so elements neither grow with larger windows nor shrink with smaller ones.
   - [x] Use theme images from `game/` for menu backgrounds with fallbacks.
   - [x] Default the window to a 16:9 resolution for consistent layouts on desktop and phone builds.
   - [x] Verify layouts match the design at common resolutions.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
   - [x] Fix residual window-size scaling bug causing janky resizing.
* [ ] UI system overhaul (`b348c09e`) – rebuild menus and in-run UI to resolve layout and theming issues.
   - [x] Stabilize background colors and prevent unintended scrolling.
   - [x] Apply scaling helper so elements no longer stretch horizontally.
   - [x] Align Home, Pulls, and Crafting buttons horizontally at the top-left.
   - [ ] Theme Edit Player and Options menus with proper backdrops and show a player preview.
   - [ ] Remove tiny tooltips and doubled button backgrounds in the Load Run menu.
   - [ ] Restore character picker for New Run and display the map with icons arranged bottom to top.
   - [ ] Add a top-right hamburger menu during runs to open settings via touch.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Project scaffold (`0f95beef`) – move legacy code, initialize uv project, install Panda3D, and set up assets and package structure.
   - [x] Move existing Pygame code into `legacy/` and keep it read-only.
   - [x] Run `uv init` to create a fresh environment.
   - [x] Install Panda3D and optional LLM tooling via `uv add panda3d` and `uv add --optional llm`.
   - [x] Add `main.py` that launches `ShowBase` and renders a placeholder cube to verify the engine.
   - [x] Scaffold directories: `assets/models/`, `assets/textures/`, `assets/audio/`, `plugins/`, `mods/`, and `llms/`.
    - [x] Include player photos with fallback images in the asset pipeline.
   - [x] Organize source under a `game/` package with `actors/`, `ui/`, `rooms/`, `gacha/`, and `saves/` submodules.
   - [x] Document the new directory structure in `README.md` and warn contributors not to modify `legacy/`.
   - [x] Define `pyproject.toml` with package name `autofighter` and expose an entry point for `main.py`.
   - [x] Research publishing `autofighter` to PyPI and note considerations for native dependencies.
   - [x] Commit minimal setup once `main.py` runs.
    - [x] Populate `game/__init__.py` so the package exports modules.
    - [x] Document this feature in `.codex/implementation`.
     - [x] Add unit tests covering success and failure cases.
* [ ] Main loop and window handling (`869cac49`) – create ShowBase subclass and handle window events.
   - [x] Expand `main.py` with a `ShowBase` subclass to manage the app lifecycle.
   - [x] Route events through Panda3D's `messenger` and schedule updates with `taskMgr`.
   - [x] Add a lightweight scene manager for swapping menus, gameplay states, and overlays.
   - [x] Handle window close events and keyboard input for quitting the game.
   - [x] Set the window title to the game's name.
    - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Scene manager (`dfe9d29f`) – swap menus, gameplay scenes, and overlays.
   - [x] Create a manager class to load and unload scenes.
   - [x] Support pushing overlays and popping back to previous scenes.
   - [x] Provide hooks for transition effects and cleanup.
   - [x] Surface and recover from scene load errors.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [ ] Plugin loader (`56f168aa`) – discover player, foe, passive, DoT, HoT, weapon, and room plugins.
   - [x] Implement a loader that discovers Python modules under `plugins/` and registers them with the game.
   - [x] Provide hooks for player, weapon, foe, passive, DoT, HoT, and room plugins.
   - [x] Expose a mod interface and avoid importing legacy Pygame code.
   - [x] Wrap Panda3D's `messenger` with an event bus so plugins can subscribe and emit without engine imports.
   - [x] Document the plugin API and how to add new plugins.
   - [x] Document this feature in `.codex/implementation`.
    - [x] Discover optional modules under `mods/` and test mod loading.
   - [x] Add unit tests covering success and failure cases.
* [x] Event bus wrapper (`120c282f`) – expose decoupled messaging so plugins can emit and subscribe.
   - [x] Wrap Panda3D's `messenger` with subscribe and emit helpers.
   - [x] Prevent plugin crashes from propagating through the bus.
   - [x] Document available events and usage.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Stats dataclass (`751e73eb`) – share core attributes between players and foes.
   - [x] Define fields for HP, attack, defense, and other core stats.
   - [x] Support additive and percentage modifiers for stat changes.
   - [x] Integrate with damage and healing modules.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Damage and healing migration (`7b715405`) – port DoT/HoT logic into new architecture.
   - [x] Define a shared `Stats` dataclass for players and foes.
   - [x] Reimplement DoT and HoT handling using Panda3D-friendly data structures.
   - [x] Support the following DoTs with their effects: Bleed, Celestial Atrophy, Abyssal Corruption, Abyssal Weakness, Gale Erosion, Charged Decay, Frozen Wound, Blazing Torment, Cold Wound (5-stack cap), Twilight Decay, Impact Echo.
   - [x] Support HoTs: Regeneration, PlayerName's Echo, PlayerName's Heal.
   - [x] Ensure stacking and reset rules match the current game's mechanics and clear after battles unless made permanent.
   - [x] Add unit tests for each damage and healing type.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [ ] Main menu (`0d21008f`) – themed entry screen with New Run, Load Run, Edit Player, Options, and Quit.
   - [x] Create a main menu with buttons for New Run, Load Run, Edit Player, Options, and Quit.
   - [x] Implement Options submenu with sound-effects volume, music volume, and toggle for stat-screen pause behaviour.
   - [x] Ensure keyboard and mouse navigation using DirectGUI with dark, glassy themed widgets.
   - [x] Apply Arknights-style layout: anchor a 2×3 high-contrast grid of Lucide icons (including **Give Feedback**) near the bottom edge, add a central banner, a top bar with player avatar, name, and currencies, and quick-access corner icons.
   - [x] Render a full-screen backdrop of slowly shifting dark color clouds so icons remain clear.
   - [x] Replace placeholder top bar and banner with avatar and themed art.
    - [x] Stub actions: New Run starts new state, Load Run lists save slots, Edit Player opens customization.
    - [x] Document this feature in `.codex/implementation`.
    - [x] Add unit tests covering success and failure cases.
* [x] Run start and map display (`dc3d4f2e`) – start a new run, show a basic map, and route to a placeholder room.
   - [x] Start a run state when New Run is selected.
   - [x] Display a simple floor map after initializing the run.
   - [x] Remove placeholder menu code and wire the scene manager.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
   - [x] Verify battle room loads required models after loader API fix.
* [x] Placeholder room (`344b9c4a`) – load a single unthemed battle room.
   - [x] Define a minimal room scene and enter it from the map.
   - [x] Return to the map when the room is cleared.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Character types (`f20caf99`) – Type A (Masculine), Type B (Feminine), Type C (Androgynous).
   - [x] Create an enum for the three body types.
   - [x] Tag player and plugin characters with their type.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [ ] Legacy character import (`7406afba`) – add all characters from the Pygame version.
   - [x] Port stats and abilities for Ally, Becca, Bubbles, Carly, Chibi, Graygray, Hilander, Kboshi, Lady Darkness, Lady Echo, Lady Fire and Ice, Lady Light, Luna, Mezzy, Mimic, and others.
   - [x] Recreate characters in the new architecture without reusing legacy code.
   - [x] Verify each character loads as a plugin.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
   - [ ] Populate missing stats and abilities for each character plugin.
* [x] Party picker (`f9c45e2e`) – choose four owned characters plus the player for each run.
   - [x] Build a selection UI listing owned characters with type icons.
   - [x] Allow runs to start with one to five party members, always including the player; cap at five.
   - [x] Persist the selected party into the new run state.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Options submenu (`8e57e5f2`) – sound-effects volume, music volume, and stat-screen pause toggle.
   - [x] Implement sound-effects and music volume sliders tied to the audio system.
   - [x] Provide a toggle for pausing the stat screen during gameplay.
   - [x] Persist settings across sessions.
   - [x] Move submenu into dedicated `game/ui/options.py` referenced by the main menu.
   - [x] Document control icons and labels in `.codex/instructions/options-menu.md`.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [ ] Player customization (`f8d277d7`) – body types, hair styles, colors, and accessories.
   - [ ] Allow players to choose among Type A (Masculine), Type B (Feminine), and Type C (Androgynous) body types.
   - [ ] Provide hair styles, colors, and accessory options.
   - [ ] Save the chosen appearance for use in runs.
   - [ ] Assign color themes to player models and ensure each body type has a 3D model.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [x] Stat allocation (`4edfa4f8`) – 100‑point pool granting +1% increments per stat.
   - [x] Provide UI for distributing points among core stats.
   - [x] Clamp allocations to remaining points and enforce the +1% rule.
   - [x] Display remaining points and prevent confirmation until all available points, including any bonus points, are spent.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Item bonus confirmation (`c0fd96e6`) – ensure upgrade-item points persist after player creation.
   - [x] Track spending of 4★ upgrade items—acquired via purchase or crafting—and apply bonus stat points as normal allocations.
   - [x] Warn when items are insufficient or bonuses exceed limits.
   - [x] Persist purchased bonuses to saves and the stat screen.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Stat screen display (`58ea00c8`) – grouped stats, status effects, and relics.
   - [x] Display core stats: HP, Max HP, EXP, Level, EXP buff multiplier, Actions per Turn.
   - [x] Show offense stats: Attack, Crit Rate, Crit Damage, Effect Hit Rate, base damage type.
   - [x] Show defense stats: Defense, Mitigation, Regain, Dodge Odds, Effect Resistance.
   - [x] Show vitality and advanced stats including Action Points, cumulative damage taken/dealt, and kills.
   - [x] List active passives, DoTs, HoTs, damage types, and relic stacks, including all effects from the planning document.
   - [x] Refresh the screen at a user-defined rate (default every 5 frames, adjustable 1–10).
   - [x] Allow ESC or close to return to the previous scene, respecting the Options pause setting.
   - [x] Expose hooks for plugins to append custom lines to the Status section.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Stat screen refresh control (`5855e3fe`) – configurable update frequency.
   - [x] Default refresh rate to every 5 frames.
   - [x] Let players choose a rate from 1 to 10 frames.
   - [x] Respect the pause setting from the Options menu.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [ ] Battle room core (`1bfd343f`) – combat scenes with stat-driven accuracy.
   - [x] Render player and foe models or placeholders using Panda3D node graphs.
   - [x] Implement turn-based logic using messenger events and the shared `Stats` dataclass for accuracy and damage.
   - [x] Scale foes according to floor, room, Pressure level, and loop count.
   - [x] Display damage numbers, status effect icons, and reusable attack effects.
   - [x] Trigger overtime warnings after 100 turns (500 for floor bosses) with red/blue flashes and an `Enraged` buff.
   - [ ] Build a functional 3D battle environment instead of placeholders.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Overtime warnings (`4e282a5d`) – flash room after 100 turns or 500 on floor bosses.
   - [ ] Count turns during battles and detect overtime thresholds.
   - [ ] Trigger visual or audio cues when overtime begins.
   - [ ] Reset the warning after combat ends.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [x] Rest room features (`5109746a`) – healing or item trades with per-floor limits.
   - [x] Offer choices to heal or trade upgrade items for benefits.
   - [x] Animate a brief rest scene to communicate outcomes.
   - [x] Track rest usage per floor, ensuring at least two rest rooms appear on each floor.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [ ] Shop room features (`07c1ea52`) – sell upgrade items and cards without rerolling.
   - [x] Design a shop interface listing items with prices, star ratings, and limited stock.
   - [ ] Implement purchasing logic that deducts gold and grants items; remove the reroll option.
   - [ ] Persist purchases between visits.
   - [x] Ensure at least two shop rooms appear per floor and inventory scales with difficulty.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Event room narrative (`cbf3a725`) – deterministic choice outcomes.
   - [x] Define an event framework with text prompts, selectable options, and seeded randomness.
   - [x] Implement chat rooms where players can send one message to an LLM character, limited to six chats per floor.
   - [x] Provide at least two sample events affecting player stats or items.
   - [x] Ensure events triggered after battles do not consume the floor's room count.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
   - [ ] Add branching options and failure-path tests to events.
* [ ] Map generator (`3b2858e1`) – 45-room floors and looping logic.
   - [ ] Generate 45-room floors containing rest, chat, battle-weak, battle-normal, battle-boss, battle-boss-floor, and shop nodes.
   - [ ] Ensure each floor has at least two shops and two rest stops; chats occur after fights without consuming room count.
   - [ ] Support Pressure Level selection that scales foes and adds rooms or bosses at specified intervals.
   - [ ] Loop maps endlessly after the final floor with enemy scaling per loop.
   - [ ] Render a color-coded vertical map showing room connections, current location, and valid paths.
   - [ ] Seed each floor from a run-specific base seed and forbid seed reuse.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Pressure level scaling (`6600e0fd`) – adjust foe stats, room counts, and extra bosses.
   - [ ] Scale foe stats proportionally to pressure.
   - [ ] Modify floor layouts to add rooms or branches as pressure increases.
   - [ ] Spawn extra bosses at high pressure thresholds.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Boss room encounters (`21f544d8`) – implement standard boss fights and fix `foe_attack` referencing an undefined `attack_button`.
   - [ ] Load boss-specific scenes, assets, and music.
   - [ ] Define unique attack patterns and rewards for each boss.
   - [ ] Transition back to the map and grant loot after victory.
   - [ ] Ensure `foe_attack` logic does not reference missing UI elements like `attack_button`.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Floor boss escalation (`51a2c5da`) – handle difficulty spikes and rewards each loop.
   - [ ] Boost boss stats and mechanics after every loop.
   - [ ] Scale loot tables to match higher difficulty.
   - [ ] Sync escalation with pressure level progression.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Chat room interactions (`4185988d`) – one-message LLM chats after battles.
   - [ ] Load a chat scene that appears after combat.
   - [ ] Send the player's message to the configured LLM and display its response.
   - [ ] Provide a skip option to return to the map quickly.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Reward tables (`60af2878`) – define drops for normal, boss, and floor boss fights.
   - [ ] Create weighted reward pools for each fight type.
   - [ ] Include upgrade items, cards, and rare drops with probabilities.
   - [ ] Integrate reward tables into battle resolution.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Gacha pulls (`4289a6e2`) – spend upgrade items on character rolls.
   - [ ] Seed the pull pool with existing player plugins and allow 1, 5, or 10 pulls.
   - [ ] Play a skippable video keyed to the highest rarity obtained and show a results menu afterward.
   - [ ] Apply pity logic starting at 0.001%, rising to ~5% at pull 159, and guaranteeing the featured character at 180 pulls.
   - [ ] Handle duplicate logic: 25% chance before completing the 5★ roster, weighted duplicates after the roster is full.
   - [ ] Grant upgrade items on failed pulls based on damage types, with item costs for upgrading and trading 10×4★ items for an extra pull.
   - [ ] Provide upgrade items for each damage type—Generic, Light, Dark, Wind, Lightning, Fire, Ice—in 1★–4★ tiers; player stat upgrades require one 4★ item from every non-Generic type.
   - [ ] Implement Vitality bonus stacking for duplicates (0.01% first, each increment +5% more than the last).
   - [ ] Serialize rewards, pity counts, and character stacks for persistence.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Gacha pity system (`f3df3de8`) – raise odds until a featured character drops.
   - [ ] Track consecutive pulls without the featured character.
   - [ ] Raise drop rates according to the pity curve and guarantee at 180 pulls.
   - [ ] Reset pity after obtaining the featured character.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [x] Duplicate handling (`6e2558e7`) – enforce stack rules and apply stat bonuses, not just Vitality.
   - [x] Detect duplicates and stack them per character.
   - [x] Grant Vitality bonuses with each duplicate according to rules.
   - [x] Apply duplicate stacks to relevant stats (e.g., increasing increments by 5% per stack) and enforce stacking behaviour.
   - [x] Update save data and roster displays after stacking.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [x] Gacha presentation (`a0f85dbd`) – implement `play_animation` and render a results menu after pulls.
   - [x] Play a skippable animation tied to the highest rarity pulled.
   - [x] Display a results screen listing characters and rewards.
   - [x] Support single and multi-pull presentations.
   - [x] Implement `play_animation` to actually play the video clip.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
* [ ] Upgrade item crafting (`418f603a`) – combine lower-star items into higher ranks.
   - [ ] Allow conversion of 125×1★ to 1×2★, 125×2★ to 1×3★, and 125×3★ to 1×4★ items.
   - [ ] Support dual-type requirements for upgrading dual-element characters.
   - [ ] Permit trading 10×4★ items for an extra gacha pull.
   - [ ] Provide a UI panel for crafting and confirming conversions.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Item trade for pulls (`38fe381f`) – exchange 4★ items for gacha tickets.
   - [ ] Provide a trade interface within the gacha menu.
   - [ ] Deduct items and grant a ticket when the trade is confirmed.
   - [ ] Prevent trades when the player lacks sufficient items.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] SQLCipher schema (`798aafd3`) – store run and player data securely.
   - [ ] Integrate SQLCipher to store run and player data with batched writes and compact schemas.
   - [ ] Derive encryption keys from a user-supplied salted password and store them in encrypted config with optional cloud backup.
   - [ ] Provide migration tooling for legacy saves using versioned scripts.
   - [ ] Explore alternative key sources such as OS keyrings, environment variables, or hardware tokens.
   - [ ] Wrap database access in a `SaveManager` with context-managed sessions.
   - [ ] Document backup, recovery, and key management steps.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Save key management (`428e9823`) – derive and back up salted-password keys.
   - [ ] Generate keys from a salted user password.
   - [ ] Store a backup copy in a secure location.
   - [ ] Rotate keys and re-encrypt saves when the password changes.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Migration tooling (`72fc9ac3`) – versioned scripts for forward-compatible saves.
   - [ ] Track schema versions and available migrations.
   - [ ] Apply migrations automatically when loading older saves.
   - [ ] Document how to add new migration steps.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Asset style research (`ad61da93`) – choose art direction and free model sources.
   - [ ] Research low-poly or pixelated 3D art styles and evaluate free/CC model sources for compatibility.
   - [ ] Establish a conversion workflow (e.g., Blender to `.bam`/`.egg`) with cached builds.
   - [ ] Maintain `assets/` structure for models, textures, and audio, and create an `assets.toml` manifest mapping keys to paths and hashes.
   - [ ] Build an `AssetManager` that loads and caches models, textures, and sounds on demand.
   - [ ] Document guidelines for artists to contribute compatible assets.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Conversion workflow (`10bd22da`) – build pipeline to Panda3D formats.
   - [ ] Define steps to export models and textures to `.bam` or `.egg`.
   - [ ] Cache converted assets to avoid redundant work.
   - [ ] Integrate the conversion into the build pipeline.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] AssetManager with manifest (`d5824730`) – load and cache assets via `assets.toml`.
   - [x] Create an `assets.toml` mapping logical keys to file paths and hashes.
   - [x] Build an AssetManager to load and cache models, textures, and sounds.
   - [x] Expose a simple API for other systems to request assets by key.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases, including missing entries and cache reuse.
   - [x] Handle Panda3D camelCase vs snake_case loader APIs for runtime compatibility.
* [ ] Audio system (`7f5c8c36`) – play music and effects with volume control.
   - [x] Set up an audio manager for playing background music and sound effects with volume controls tied to settings.
   - [x] Implement cross-fades for boss themes and overtime warnings after long battles.
   - [x] Support toggling stat-screen pause behaviour for audio if needed.
   - [x] Document this feature in `.codex/implementation`.
   - [x] Add unit tests covering success and failure cases.
   - [ ] Use real Panda3D sound playback in tests.
* [ ] UI polish and accessibility (`d6a657b0`) – dark glass theme, color-blind mode, keyboard navigation.
   - [ ] Implement dark, glassy theme with blurred gradient backgrounds, rounded panels, and accent highlights.
   - [ ] Provide color-blind friendly options and ensure star colors (1 gray, 2 blue, 3 green, 4 purple, 5 red, 6 gold) are readable.
   - [ ] Audit keyboard-only navigation and scalable layouts for desktop and mobile resolutions.
   - [ ] Offer settings to adjust or disable overtime warning colors and speed.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Documentation and contributor guidelines (`ca46e97e`) – update README and contributor docs for new structure.
   - [ ] Write developer setup steps for installing dependencies with `uv` and running `main.py`.
   - [ ] Outline coding style and directory conventions for the new `game/` package and `assets/` structure.
   - [ ] Warn contributors not to modify `legacy/` and explain plugin documentation expectations.
   - [ ] Provide guidelines for contributing plugins and assets, including the `Give Feedback` menu and issue links.
   - [ ] Require developers to use a Panda3D-enabled environment and verify APIs against the official docs (https://docs.panda3d.org/).
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Testing and CI integration (`93a6a994`) – add headless tests, GitHub workflows, and run `uv run pytest` last.
   - [ ] Add unit tests for menus, stat screen, map navigation, gacha logic, and data wiring under `tests/`.
   - [ ] Configure headless Panda3D fixtures to run in CI.
   - [ ] Create a GitHub Actions workflow to run `uv run pytest` and lint on pushes and pull requests.
   - [ ] Document how to run tests locally.
   - [ ] Audit `builder/` scripts for Windows, Linux, and Android.
   - [ ] Verify Panda3D and dependency bundling for each platform.
   - [ ] Perform smoke builds on supported platforms to catch cross-OS issues.
   - [ ] Document this feature in `.codex/implementation`.
   - [ ] Add unit tests covering success and failure cases.
* [ ] Feedback menu button (`2a9e7f14`) – open a pre-filled GitHub issue from the in-game menu.
    - [x] Add a `Give Feedback` option to the main menu.
    - [x] Launch the user's browser with a pre-filled GitHub issue template.
    - [x] Document this feature in `.codex/implementation`.
    - [x] Add unit tests covering success and failure cases.
* [ ] Initial cards and relics (`16e6e663`) – seed starting rewards.
    - [ ] Create 10 1★ cards and relics.
    - [ ] Create 5 2★ cards and relics.
    - [ ] Create 2 3★ cards and relics.
    - [ ] Create 2 4★ cards and relics.
    - [ ] Create 2 5★ cards and relics.
    - [ ] Implement cards and relics as plugins like players and DoT/HoT effects.
    - [ ] Document this feature in `.codex/implementation`.
    - [ ] Add unit tests covering success and failure cases.
* [ ] Player model color themes (`3ee1be05`) – assign palettes to player objects.
    - [ ] Define a color theme for each player plugin's model.
    - [ ] Apply themes during rendering so characters reflect their palette.
    - [ ] Document this feature in `.codex/implementation`.
    - [ ] Add unit tests covering success and failure cases.
## Context
Derived from the Panda3D game plan and existing Panda3D remake task list to coordinate development.

# Panda3D Game Remake Planning

## Goal
Fully remake the Pygame-based roguelike autofighter in Panda3D with 3D-ready architecture while retaining plugin-driven combat, menus, stat screens, and a multi-room run map.

## Project Lead Feedback
- Redesign the main menu with a high-contrast grid of large icons inspired by Arknights.
- Standardize on Lucide icons and provide clear labels for every menu item.
- Audit Player and Settings menus for missing labels and verify UI scaling, font sizes, and DPI handling.
- Menus use a global DirectGUI scaling system anchored to 16:9 so layouts stay consistent across window sizes and follow the requested layout.
- Menu backgrounds pull from themed images with fallbacks, and the window defaults to a 16:9 resolution so desktop and phone builds share the same layout.
- Create an initial set of cards and relics (10×1★, 5×2★, 2×3★, 2×4★, and 2×5★) using the plugin system like players and effects.
- Fix the shop so purchases persist and remove reroll mechanics.
- Confirm the battle room includes a functional 3D space.
- Ensure all three body types have working models.
- Apply color themes to player objects.
- Maintain `myunderstanding.md` with an up-to-date gameplay overview.
- Map scene now loads player models after the asset loader was expanded
  to handle both camelCase and snake_case Panda3D APIs; tests verify the
  battle room attaches models correctly.
- Window resize events are clamped back to 16:9 so menus keep their
  layout instead of scaling with the window size.
- The main menu top bar now displays the player portrait and themed banner art.

## Current Issues
- Main menu background shifts colors and scrolls unexpectedly.
- UI elements stretch horizontally; scaling helper not applied consistently.
- Edit Player and Options menus lack themed backgrounds and a player preview.
- Load Run entries show tiny tooltips and duplicated button backdrops.
- New Run skips the character picker, opens a black scene, and fails to load the map.
- Map display uses placeholder text (e.g., reversed "BNSHBW"); should show icons from bottom to top and scroll vertically.
- Runs need a top-right hamburger menu to access settings via touch.
- Developers must work in a Panda3D-enabled environment and consult the official Panda3D docs (https://docs.panda3d.org/) instead of guessing APIs.

## Immediate Playable Flow
1. Finalize the main menu so New Run can trigger the gameplay loop.
2. Initialize a run when New Run is selected and show a basic floor map.
3. Allow entering a single unthemed placeholder room from the map and returning afterward.
4. Define character types: Type A (Masculine), Type B (Feminine), and Type C (Androgynous).
5. Import all characters from the Pygame version and tag them with their type.
6. Provide a party picker that lets the player choose four owned characters plus the player.
7. Use the selected party to begin the run.

## Detailed Plans
- [Project Setup](f94337b7-project-setup-plan.md)
- [Core Architecture](8aabf6d1-core-architecture-plan.md)
- [UI Foundation](e26e5ed7-ui-foundation-plan.md)
- [Player Stat Screen](a28124e9-player-stat-screen-plan.md)
- [Map and Room Types](e158df1a-map-and-room-types-plan.md)
- [Gacha Character Recruitment](82dc97b7-gacha-character-recruitment-plan.md)
- [Encrypted Save System](43054f8b-encrypted-save-system-plan.md)
- [Asset Pipeline](0c92aee1-asset-pipeline-plan.md)
- [Testing and Iteration](0fc17c39-testing-and-iteration-plan.md)

## Open Questions
- Where should DoT, passive, and damage-type info appear on the stat screen for best readability? Separate tabs or a scrollable list?
- How should we balance 5★ rates against extremely rare 6★ dual-type characters and set pity thresholds?
- What UX should crafting menus use to convert upgrade items or trade them for pulls?
- Which additional options should testers tweak for stat-screen pause behaviour, game speed, or accessibility?
- How should key backups be handled across platforms for the salted-password save encryption?
- Should **Pressure Level** remain the final name for the difficulty slider, and is showing it as `Name (5)` over foe heads clear enough to distinguish it from room-based enrages?
- Do the proposed star colors (1 gray, 2 blue, 3 green, 4 purple, 5 red, 6 gold) read well across UI elements and loot types? This needs playtesting once the UI exists.
- What flash rate and intensity keep the red/blue overtime warning noticeable without causing discomfort? Allow users to adjust color, speed, or disable it entirely.

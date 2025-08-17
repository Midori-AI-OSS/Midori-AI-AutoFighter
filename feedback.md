 # Feedback Log

- Date: 2025-08-15
- Author(s): Lead Dev, GitHub Copilot

Summary:

- Initial feedback entries consolidated into a single log.

Details:

2) Crafting menu icons missing (In testing)
- Symptom: Crafting list displays item names and counts but icons and star-rank outlines are missing (no visual sprites displayed).
- Impact: Harder to scan materials and identify rarities quickly; reduces UI polish and can confuse players.
- Suggested follow-up: Verify asset paths and rendering logic for crafting items; check CSS rules that may hide background images or SVG icons. Add a fallback placeholder icon when assets fail to load.

3) Crafted items do not stack and names are janky (In testing)
- Symptom: Crafted items in the crafting menu do not stack (e.g., 8x 4-star ice items show as 8 separate entries) and names are displayed poorly.
- Impact: Inventory is cluttered and hard to read; user cannot easily see total counts of each item.
- Suggested follow-up: Update UI and logic to stack items by type and rarity, and improve name formatting for clarity.

4) Settings wipe data does not wipe data
- Symptom: In settings, the 'wipe data' button is unclickable or gives no feedback on the frontend if it worked...
- Impact: Users unsure if wipe worked...

5) Party & Character picker issues (FAILED TESTING, WAS NOT WORKED ON, FIX!)
- Symptom: Chars the player does not have due to wiping data still showing up in the party picker.
- Symptom: Multiple UI and data inconsistencies observed:
  - Party picker: player type is incorrect (player showing Fire instead of Light) because Player Editor settings are not persisting.
  - DEF is currently under the Core tab; should be at the top of the Defense tab.
  - EXP is placed at the bottom of the Core tab; should appear under HP.
  - Character picker: type icon uses the wrong color (e.g., Becca's icon is white, should be damage type color) and the character box outline color is incorrect.
  - Character picker layout shows multiple characters per row; should display one character per row for readability.
- Impact: Confusing stat layout, incorrect visuals, and mismatched player types can cause gameplay errors and poor UX.
- Suggested follow-up: Reconcile Player Editor persistence first, then audit the character picker rendering and CSS (icon colors, outline colors, layout grid). Reorder stat placement in the UI and add tests to verify correct stat positions and type assignment. Fix damage type icon color for Becca and others.

7) Map & Battle UI issues
- Map room scrolling:
  - Symptom: Map requires manual scrolling to bottom to view content; players should only need to see next 4 room groups instead of full map scroll.
  - Suggested follow-up: Implement viewport clipping or pagination to show only the next 4 room groups; reduce DOM nodes rendered for performance.

- Status: Map component now slices the run's rooms with `map.slice(-4)` to limit rendering and trim excess DOM nodes.

- Battle UI issues (start of battle / in-battle):
  - Missing party member icons and unknown damage types for characters — party members render without icons, likely missing asset loading or incorrect type mapping.
  - Rewards menu appears unthemed and outside of the battle viewport; right sidebar remains visible inside battle window.
  - Battle background not visible inside battle UI (background missing/clipped).
  - UI layout/positioning is janky on battle start (overlapping elements, sidebar bleeding into viewport).
  - Suggestion: Reuse party picker asset loading and type mapping; add a small shared utility to normalize character asset loading across modules.

- Suggested follow-up: Capture DOM/network during battle start, compare party picker asset load sequence, and ensure battle viewport isolates/hides non-battle UI (sidebars). Create issues with reproduction steps and sample network logs.




# Gameplay Overview

*Current status:* The **Start Run** button now hits the backend and opens the floor map with the generated rooms. The map shows the boss at the top, grays out future rooms, and keeps the current room highlighted at the bottom. Clicking the highlighted node posts an empty `action` to the backend and resolves the encounter. Rooms without a dedicated endpoint can fall back to `/rooms/{run_id}/{room_id}/action`, which echoes the sent `action`. Battles now play out entirely on the server until either side is defeated, processing passives, cards, relics, and DoT/HoT effects each turn with a brief async pause between turns.

Damage types can now inflict element-themed DoTs by rolling the attacker's `effect_hit_rate` against a target's `effect_resistance`. The difference is clamped to zero, jittered by ±10%, and there's always a 1% floor chance to land the status. The event bus broadcasts `damage` and `heal` events whenever numbers change so passives and relics can react.

When I first load the web game I see a dark, glassy main menu with buttons for **Run**, **Map**, **Party**, **Edit**, **Pulls**, **Craft**, **Settings**, and **Stats**. A stained-glass bar in the top-left now works: the **Home** diamond returns to the main menu, the **User** icon opens the Player Editor, the **Settings** cog opens configuration, and the **Back** arrow steps to the previous screen. I can choose allies and set damage types, and starting a run now works. The backend already has routes for battles, shops, and rests, and the frontend now checks for active battles and locks other menus during combat.

To get the game playable, the map now mimics Slay the Spire with the boss at the top and the path rising upward. Finished rooms disappear so I can see my progress.

After each battle the backend may return card choices; the viewport now opens a reward overlay with art from `src/lib/assets` so I can pick one before moving on.

This is my current understanding of how the game behaves. I'll update it as new pieces fall into place.

The frontend now ships 24×24 placeholder icons for items, relics, and cards, organized by damage type or star rank so art can drop in later.

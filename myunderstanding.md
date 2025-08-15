# Gameplay Overview

*Current status:* Run, Map, Character Editor, Pulls, Crafting, Stats, and a columned Settings menu with framerate and autocraft controls are functional.

When I launch the web-based game the Svelte frontend shows a dark, glassy main menu rendered as a high-contrast icon grid. Buttons include **Run**, **Map**, **Party**, **Edit**, **Pulls**, **Craft**, **Settings**, and **Stats**, each with a Lucide icon and label. Pressing **Run** opens a modal party picker over a random backdrop. The frontend asks the backend for the full plugin roster and only shows entries I own, with my avatar pinned to the top. I can add up to four allies beneath it, view each character's passive, and change my own damage type to Light, Dark, Wind, Lightning, Fire, or Ice. After confirming, the frontend calls the Quart backend to start a new run, returning a run ID and a generated map that the backend writes to `backend/save.db` so progress survives restarts (plaintext by default; set `AF_DB_KEY` or `AF_DB_PASSWORD` to enable SQLCipher encryption). The **Pulls** button opens a gacha menu that shows my pity counter and tickets, letting me spend upgrade items on `/gacha/pull`; failed pulls award element-specific 1★–4★ items. The **Craft** button reveals a menu to convert upgrade items and toggle automatic crafting via `/gacha/craft` and `/gacha/auto-craft`. Successful rolls recruit 5★ or very rare 6★ characters and reset the pity counter.

A row of stained-glass buttons with `lucide-svelte` icons appears for the seeded 45-room floor. Nodes include shops, rests, battle-weak, battle-normal, and a final battle-boss-floor. Tapping a button calls the matching Quart endpoint and shows a view with foes arrayed across the top and my party on the bottom, each ally tagged with a small ultimate circle.

On a desktop monitor the interface now devotes roughly 95% of the screen to the game viewport, framed by a stained-glass sidebar for menu actions. A Player Editor lets me set pronouns up to fifteen characters, switch my damage type, and distribute stat points before a run. Tablets show the menu beside the party picker, while phones limit the view to one menu at a time so navigation stays simple.

Battle rooms trigger passives and have my team automatically trading blows with a scaled Slime while damage numbers and status icons pop up. Winning a battle presents three unused cards based on star rank; picking one adds it to our shared list, and its bonus kicks in at the start of the next combat alongside relic effects. Entering a shop heals the party by 5% of its combined max HP before displaying items with prices and star ratings, letting me spend gold or reroll the stock. Rest rooms offer a calm break to pull from the gacha with shared pity, craft items, swap party members on the spot, and occasional chat scenes echo a single message from an LLM copy of a character without consuming room count. New characters from these pulls land in `owned_players` right away, so I can slot them into the party before moving on.

Along the way I'll collect cards and relics in a shared party inventory. Cards give small stat boosts or special perks and relics provide stronger passive effects; both reapply when a battle begins.

Clearing room after room will eventually bring me to a boss icon. Beating the boss finishes the floor and I'll return to the map or the main menu. Between runs or at rests I can roll the gacha for new characters (drawing from the same pity and currency), set custom pronouns up to fifteen characters, choose any base damage type—Light, Dark, Wind, Lightning, Fire, or Ice—for free, and allocate starting stats that boost HP, Attack, and Defense by 1% per point. Luna's Generic damage type is reserved for her and can't be selected. Stats and damage type lock once a run begins.

Any character marked as having a random damage type rolls their element once and
keeps that choice on future loads.

Placeholder menus now cover card and relic inventories, battle screens, map displays, rest rooms, and shops, each wrapped in the shared frosted `MenuPanel` for a consistent look.

This document reflects how the game currently plays and should be kept up to date as features evolve.

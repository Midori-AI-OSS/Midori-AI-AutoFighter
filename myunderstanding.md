# Gameplay Overview

When I launch the web-based game the Svelte frontend shows a dark, glassy main menu rendered as a high-contrast icon grid. A slim top bar displays my small avatar, name, and pull count. A frosted panel hugs the upper-left corner with a horizontal row of **Avatar**, **Pulls**, and **Crafting** buttons, each icon perched above its label. The right side pushes a vertical stack of **Run**, **Edit Player**, **Settings**, and **Quit** further to the edge so their labels sit beside their icons. Curious, I press **Run** and a modal party picker fades in over a random backdrop. The frontend asks the backend for the full plugin roster and only shows entries I own, with my avatar pinned to the top. I can add up to four allies beneath it, view each character's passive, and change my own damage type to Light, Dark, Wind, Lightning, Fire, or Ice. After confirming, the frontend calls the Quart backend to start a new run, returning a run ID and a generated map that the backend writes to `backend/save.db` so progress survives restarts (plaintext by default; set `AF_DB_KEY` or `AF_DB_PASSWORD` to enable SQLCipher encryption).

A row of room buttons appears for the seeded 45-room floor. Nodes include shops, rests, battle-weak, battle-normal, and a final battle-boss-floor. Tapping a button calls the matching Quart endpoint and shows a view with foes arrayed across the top and my party on the bottom, each ally tagged with a small ultimate circle.

On a desktop monitor the party picker, player editor, and a stats panel flank the main menu. Tablets show the menu beside the party picker, while phones limit the view to one menu at a time so navigation stays simple.

The frontend polls the backend's `/player/stats` endpoint to fill that panel, which returns grouped stats and a `refresh_rate` clamped between 1 and 10 frames.

Battle rooms trigger passives and have my team automatically trading blows with a scaled Slime while damage numbers and status icons pop up. Winning a battle presents three unused cards based on star rank; picking one adds it to our shared list, and its bonus kicks in at the start of the next combat alongside relic effects. Entering a shop heals the party by 5% of its combined max HP before displaying items with prices and star ratings, letting me spend gold or reroll the stock. Rest rooms offer a calm break to heal, access the gacha with shared pity, and immediately slot newly pulled characters before leaving, and occasional chat scenes echo a single message from an LLM copy of a character without consuming room count.

Along the way I'll collect cards and relics in a shared party inventory. Cards give small stat boosts or special perks and relics provide stronger passive effects; both reapply when a battle begins.

Clearing room after room will eventually bring me to a boss icon. Beating the boss finishes the floor and I'll return to the map or the main menu. Between runs or at rests I can roll the gacha for new characters (drawing from the same pity and currency), set custom pronouns up to fifteen characters, choose any base damage type—Light, Dark, Wind, Lightning, Fire, or Ice—for free, and allocate starting stats. Luna's Generic damage type is reserved for her and can't be selected. Stats and damage type lock once a run begins.

Any character marked as having a random damage type rolls their element once and
keeps that choice on future loads.

This document reflects how the game currently plays and should be kept up to date as features evolve.

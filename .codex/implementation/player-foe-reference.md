# Player and Foe Reference

## Player Roster
All legacy characters from the Pygame version have been ported as plugins.
Each entry notes the character's `CharacterType` and starting damage type.
Players currently share placeholder stats of 1000 HP, 100 attack, 50 defense,
5% crit rate, 2× crit damage, 1% effect hit, 100 mitigation, 0 dodge, and 1
for remaining values.

- **Ally** (B, random) – applies `ally_passive` on load to grant ally-specific bonuses.
- **Becca** (B, random) – builds high attack but takes more damage from lower defense.
- **Bubbles** (A, random) – starts with a default item and applies `bubbles_passive`.
- **Carly** (B, Light) – applies `carly_passive`.
- **Chibi** (A, random) – gains four times the normal benefit from Vitality.
- **Graygray** (B, random) – applies `graygray_passive`.
- **Hilander** (A, random) – builds increased crit rate and crit damage.
- **Kboshi** (A, random) – randomly changes damage type.
- **Lady Darkness** (B, Dark) – baseline fighter themed around darkness.
- **Lady Echo** (B, Lightning) – baseline fighter themed around echoes.
- **Lady Fire and Ice** (B, Fire or Ice) – baseline fighter themed around fire and ice.
- **Lady Light** (B, Light) – baseline fighter themed around light.
- **Lady of Fire** (B, Fire) – baseline fighter themed around fire.
- **Luna** (B, Generic) – applies `luna_passive`.
- **Mezzy** (B, random) – only raises Max HP and takes less damage.
- **Mimic** (C, random) – copies the player then lowers its stats by 25% on spawn.
- **Player** (C, chosen) – avatar representing the user and may select any non-Generic damage type.

## Foe Generation
Foe plugins inherit from `FoeBase`, which mirrors `PlayerBase` stats. They are
procedurally named by pairing an adjective from `themed_ajt` with a themed name
from `themed_names` in `themedstuff.py`. After naming,
`foe_passive_builder.build_foe_stats` applies stat modifiers:

1. `_apply_high_level_lady` boosts high-level foes with *Lady* in their names,
   scaling stats by variant (Light, Dark, Fire, or Ice).
2. `_apply_themed_name_modifiers` adjusts stats based on the themed name
   (e.g., "Luna" favors dodge and defense, while "Carly" gains massive
   mitigation).
3. `_apply_themed_adj_modifiers` tweaks stats depending on the adjective
   (e.g., "Atrocious" increases attack).
4. `player_stat_picker` selects a stat tier using the themed name, influencing
   base stat scaling.

Example: **Atrocious Luna** receives dodge and defense from the "Luna" portion
and an attack boost from "Atrocious", producing a foe whose name directly
translates into combat bonuses.

Development builds include a `Slime` foe plugin that reduces all baseline stats
by 90% for simple battle testing. Standard battles may also spawn random player
characters that are not currently in the party.

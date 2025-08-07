# Player and Foe Reference

## Player Roster
All legacy characters from the Pygame version have been ported as plugins.
Each entry notes the character's `CharacterType`.

- **Ally** (B) – applies `ally_passive` on load to grant ally-specific bonuses.
- **Becca** (B) – builds high attack but takes more damage from lower defense.
- **Bubbles** (A) – starts with a default item and applies `bubbles_passive`.
- **Carly** (B) – applies `carly_passive`.
- **Chibi** (A) – gains four times the normal benefit from Vitality.
- **Graygray** (B) – applies `graygray_passive`.
- **Hilander** (A) – builds increased crit rate and crit damage.
- **Kboshi** (A) – randomly changes damage type.
- **Lady Darkness** (B) – baseline fighter themed around darkness.
- **Lady Echo** (B) – baseline fighter themed around echoes.
- **Lady Fire and Ice** (B) – baseline fighter themed around fire and ice.
- **Lady Light** (B) – baseline fighter themed around light.
- **Lady of Fire** (B) – baseline fighter themed around fire.
- **Luna** (B) – applies `luna_passive`.
- **Mezzy** (B) – only raises Max HP and takes less damage.
- **Mimic** (C) – copies the player then lowers its stats by 25% on spawn.

## Foe Generation
Foes are procedurally named by pairing an adjective from `themed_ajt`
with a themed name from `themed_names` in `themedstuff.py`. After naming,
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

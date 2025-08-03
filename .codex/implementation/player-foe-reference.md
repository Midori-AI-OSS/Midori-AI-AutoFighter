# Player and Foe Reference

## Player Roster
- **Ally** – applies `ally_passive` on load to grant ally-specific bonuses.
- **Becca** – baseline fighter with no unique starting passive.
- **Bubbles** – starts with a default item and applies `bubbles_passive`.
- **Carly** – applies `carly_passive`.
- **Chibi** – baseline fighter with no unique passive.
- **Graygray** – applies `graygray_passive`.
- **Hilander** – baseline fighter with no unique passive.
- **Kboshi** – baseline fighter with no unique passive.
- **Lady Darkness** – baseline fighter themed around darkness.
- **Lady Echo** – baseline fighter themed around echoes.
- **Lady Fire and Ice** – baseline fighter themed around fire and ice.
- **Lady Light** – baseline fighter themed around light.
- **Lady of Fire** – baseline fighter themed around fire.
- **Luna** – applies `luna_passive`.
- **Mezzy** – baseline fighter with no unique passive.
- **Mimic** – baseline fighter with no unique passive.

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

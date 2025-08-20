# Player and Foe Reference

## Player Roster
All legacy characters from the Pygame version have been ported as plugins.
Each entry notes the character's `CharacterType` and starting damage type.
Players currently share placeholder stats of 1000 HP, 100 attack, 50 defense,
5% crit rate, 2× crit damage, 1% effect hit, 100 mitigation, 0 dodge, and 1
for remaining values.

Player plugins also include a `gacha_rarity` field so the gacha system can
automatically discover 5★ and 6★ recruits.
Each player and foe defines `prompt` and `about` strings with placeholder text
to support future character-specific prompts.

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

Characters marked as "random" roll one of the six elements when first loaded
and reuse that element in future sessions.

## Foe Generation
Foe plugins inherit from `FoeBase`, which mirrors `PlayerBase` stats. To keep
encounters from stalling, foes regain health at one hundredth the player rate.
They are procedurally named by prefixing a randomly selected adjective plugin
from `plugins/themedadj` to a player name. Adjective plugins are
auto-discovered based on files in that directory, so adding a new adjective
requires only dropping a file into the folder. Each adjective class applies its own
stat changes derived from the legacy project—for example, **Atrocious** boosts
max HP by 90% and attack by 10%.

Example: **Atrocious Luna** applies the adjective's stat bonuses to the base
player stats and prefixes the foe's name, yielding a combatant whose title
reflects its enhanced abilities.

Development builds include a `Slime` foe plugin that reduces all baseline stats
by 90% for simple battle testing. Standard battles may also spawn random player
characters that are not currently in the party. These player foes are wrapped in
`FoeBase` at load time, granting them foe-specific behaviors such as periodic
HP regeneration via `maybe_regain`.

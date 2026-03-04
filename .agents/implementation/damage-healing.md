# Damage and Healing Effects

Summaries of elemental damage behaviors and ongoing effect plugins.

## Elemental Damage

- **[Generic](../../backend/plugins/damage_types/generic.py)** – Baseline element with an ultimate that splits the user's attack into 64 rapid strikes on a single target, counting each hit as a separate action.
- **[Fire](../../backend/plugins/damage_types/fire.py)** – Scales damage by missing HP and applies [Blazing Torment](../../backend/plugins/dots/blazing_torment.py), a stackable DoT that ticks when the target acts. Its ultimate hits every foe with the caster's attack and rolls Blazing Torment on each, then adds a drain stack that burns the user for 5% max HP per stack at the start of their turns.
- **[Ice](../../backend/plugins/damage_types/ice.py)** – Inflicts [Frozen Wound](../../backend/plugins/dots/frozen_wound.py), reducing `actions_per_turn` and adding a 1% miss chance per stack. Some abilities instead use [Cold Wound](../../backend/plugins/dots/cold_wound.py) which caps at five stacks. Its ultimate strikes every foe six times, with each hit in a wave dealing 30% more damage than the last target.
- **[Lightning](../../backend/plugins/damage_types/lightning.py)** – Pops every active DoT for 25% of its damage on hit and applies [Charged Decay](../../backend/plugins/dots/charged_decay.py), a DoT that stuns on its final tick.
- **[Wind](../../backend/plugins/damage_types/wind.py)** – Repeats the opening strike on each remaining foe and rolls [Gale Erosion](../../backend/plugins/dots/gale_erosion.py) on every target, trimming Mitigation each tick.
- **[Light](../../backend/plugins/damage_types/light.py)** – Creates [Celestial Atrophy](../../backend/plugins/dots/celestial_atrophy.py) and grants allies [Radiant Regeneration](../../backend/plugins/hots/radiant_regeneration.py) every action; if an ally drops below 25% HP the attack becomes a direct heal. Its ultimate fully heals allies, cleanses allied DoTs, and inflicts a 10-turn defense debuff on enemies.
- **[Dark](../../backend/plugins/damage_types/dark.py)** – Spreads [Abyssal Corruption](../../backend/plugins/dots/abyssal_corruption.py) and adds a permanent [Shadow Siphon](../../backend/plugins/dots/shadow_siphon.py) to each party member every turn. Siphon ticks drain 5% max HP and grant the Dark attacker a small temporary attack/defense boost called "Dark Resonance" based on the damage dealt as a percentage of the target's max HP.

## Supported DoTs

- [Bleed](../../backend/plugins/dots/bleed.py) – deals 2% of Max HP each turn.
- [Poison](../../backend/plugins/dots/poison.py) – deals its set damage each turn.
- [Celestial Atrophy](../../backend/plugins/dots/celestial_atrophy.py) – reduces Attack every tick.
- [Abyssal Corruption](../../backend/plugins/dots/abyssal_corruption.py) – dark damage that spreads to nearby foes when the target falls.
- [Abyssal Weakness](../../backend/plugins/dots/abyssal_weakness.py) – lowers Defense while active.
- [Gale Erosion](../../backend/plugins/dots/gale_erosion.py) – strips Mitigation each tick.
- [Charged Decay](../../backend/plugins/dots/charged_decay.py) – stuns on the final tick.
- [Frozen Wound](../../backend/plugins/dots/frozen_wound.py) – reduces Actions per Turn and adds a 1% miss chance per stack.
- [Blazing Torment](../../backend/plugins/dots/blazing_torment.py) – stackable and gains an extra tick whenever the target acts.
- [Cold Wound](../../backend/plugins/dots/cold_wound.py) – stacks up to five times.
- [Twilight Decay](../../backend/plugins/dots/twilight_decay.py) – drains Vitality per tick.
- [Impact Echo](../../backend/plugins/dots/impact_echo.py) – repeats 50% of the last damage taken for three turns.
- [Shadow Siphon](../../backend/plugins/dots/shadow_siphon.py) – infinite-duration DoT that increases its timer each tick.

## Supported HoTs

- [Regeneration](../../backend/plugins/hots/regeneration.py) – heals a flat amount each tick.
- [Player Echo](../../backend/plugins/hots/player_echo.py) – heals 20% of ally damage for a few turns.
- [Player Heal](../../backend/plugins/hots/player_heal.py) – applies an instant heal and 1% Max HP per turn.
- [Radiant Regeneration](../../backend/plugins/hots/radiant_regeneration.py) – light-aspected heal applied to allies each turn by Light attackers.

## Testing

Run `uv run pytest` to validate DoT and HoT behaviors.

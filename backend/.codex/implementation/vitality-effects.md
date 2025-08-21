# Vitality effects

- Direct healing and healing over time scale with both the healer's vitality and the target's vitality: `healing * healer_vitality * target_vitality`.
- Damage over time uses the same vitality modifiers as direct damage; source vitality increases damage while target vitality reduces it with a minimum of 1 per tick.
- Light damage type users grant all allies a stack of Radiant Regeneration
  (5 HP over 2 turns) on each action and will directly heal allies under 25%
  HP instead of attacking.

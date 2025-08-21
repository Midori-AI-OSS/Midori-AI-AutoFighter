# Vitality effects

- Direct healing and healing over time scale with both the healer's vitality and the target's vitality: `healing * healer_vitality * target_vitality`.
- Damage over time uses the same vitality modifiers as direct damage; source vitality increases damage while target vitality reduces it with a minimum of 1 per tick.
- Light damage type users grant all allies a stack of Radiant Regeneration
  (5 HP over 2 turns) on each action and will directly heal allies under 25%
  HP instead of attacking.
- Dark damage type users apply a stack of Shadow Siphon to every party member
  each action. The DoT has no turn limit and drains 5% of max HP per stack each
  tick. For every 1% of max HP drained, the Dark user gains matching attack and
  defense. All Shadow Siphon stacks are cleared when the battle ends.
- Wind damage type users strike all remaining foes after their first hit,
  repeating the damage and rolling their Gale Erosion DoT on each target.
- Frozen Wound stacks reduce actions per turn and give the afflicted unit a
  `1% × stacks` chance to miss their next action.

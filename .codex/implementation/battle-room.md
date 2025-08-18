# Battle Rooms

`BattleRoom` resolves turn-based encounters against scaled foes drawn from player plugins you haven't selected. Passives fire on room entry, battle start, and at the beginning and end of each turn. Combat continues until either every party member or the foe is defeated. The `EffectManager` applies damage-over-time and healing-over-time ticks on each combatant before actions take place, and the async loop inserts small awaits after each tick so DoTs and HoTs remain non-blocking while turns yield control back to the event loop.

Each strike rolls the attacker's `effect_hit_rate` against the target's `effect_resistance`. The difference is clamped to zero, jittered by ±10%, and even a failed roll has a 1% floor chance to attach a damage-type-specific DoT scaled to the damage dealt.

`BossRoom` subclasses `BattleRoom` but multiplies foe stats by 100× to create floor bosses.

Experience is awarded as soon as a foe falls, allowing multiple enemies to grant cumulative rewards. When the fight ends, the backend returns updated party stats, card choices, and foe data so the run map can advance.

# Loop scaling

Foe stats scale via `balance.loop.scale_stats`, multiplying base values by floor, room, and loop counts. Floor bosses apply an extra `100×` base factor. Tuning knobs live in `balance.loop.config` for adjusting loop multipliers without touching combat logic.

# Battle room rewards

Rewards draw from a Rare Drop Rate (RDR) that starts at zero and rises with floor, room index, and any bonuses from relics or cards. Higher RDR increases the odds of rarer stars while proportionally reducing common ones. Card rewards roll star ranks using these baseline odds; regular battles only offer 1★ or 2★ cards, bosses extend the table up to 5★, and floor bosses guarantee 3★ or better. Percentages below reflect baseline odds at RDR 0.

Normal fights:
- 5% chance to drop a relic (1★ at 98%, 2★ at 2%).
- Upgrade items: 80% 1★, 20% 2★.
- Cards: 80% 1★, 20% 2★.
- Gold: `5 × loop × rand(1.01, 1.25)`.

Boss fights:
- 25% chance to drop a relic (1★ 40%, 2★ 30%, 3★ 0.15%, 4★ 0.10%, 5★ 0.05%).
- Upgrade items: 60% 1★, 39.9% 2★, 0.10% 3★.
- Cards: 40% 1★, 30% 2★, 0.15% 3★, 0.10% 4★, 0.05% 5★.
- Gold: `20 × loop × rand(1.53, 2.25)`.

Floor bosses:
- Guaranteed relic drop (3★ at 0.98%, 4★ at 0.02%, 5★ at 0.0002%).
- Upgrade items: 0.8% 3★, 0.2% 4★.
- Cards: 0.6% 3★, 0.25% 4★, 0.15% 5★.

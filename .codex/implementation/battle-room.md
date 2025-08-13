
# Battle Rooms

`BattleRoom` hosts turn-based encounters against scaled foes drawn from player plugins you haven't selected. It triggers party passives, handles attack rolls, damage display, and overtime warnings after long fights.

`BossRoom` extends this scene to load boss-specific models, music, and scripted attack patterns. Boss configurations live in `autofighter.rooms.boss_patterns` and expose reward data after victory.

When the player or foe is defeated, the room exits back to the previous scene so the run map continues automatically.

The web frontend includes a placeholder `BattleView` using `MenuPanel` to reserve space for timelines and actions.

Model assets load through the shared `AssetManager`, which reads web-friendly formats through a unified loader. Tests cover setup to ensure player and foe models attach correctly when a battle begins.

# Loop scaling

Foe stats scale via `balance.loop.scale_stats`, which multiplies base values by floor, room, and loop counts. Floor bosses apply an extra `100×` base factor. Tuning knobs live in `balance.loop.config` for adjusting loop multipliers without touching combat logic.

# Battle room rewards

Rewards draw from a Rare Drop Rate (RDR) that starts at zero and rises with
floor, room index, and any bonuses from relics or cards. Higher RDR increases
the odds of rarer stars while proportionally reducing common ones. Percentages
below reflect baseline odds at RDR&nbsp;0.

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
- Pull tickets: `min(5, 1 + pressure // 20 + loop)`.
- Gold: `200 × loop × rand(2.05, 4.25)`.

Rewards are chosen when the foe falls, and the battle scene displays a summary of the loot.

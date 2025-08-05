# Battle room rewards

Normal fights:
- 5% chance to drop a relic (1★ at 98%, 2★ at 2%).
- Upgrade items: 80% 1★, 20% 2★.
- Cards: 80% 1★, 20% 2★.
- Gold: `5 × loop × rand(1.01, 1.25)`.

Boss fights:
- 25% chance to drop a relic (1★ 40%, 2★ 30%, 3★ 15%, 4★ 10%, 5★ 5%).
- Upgrade items: 60% 1★, 30% 2★, 10% 3★.
- Cards: 40% 1★, 30% 2★, 15% 3★, 10% 4★, 5% 5★.
- Gold: `20 × loop × rand(1.53, 2.25)`.

Floor bosses:
- Guaranteed relic drop (3★ at 98%, 4★ at 2%).
- Upgrade items: 80% 3★, 20% 4★.
- Cards: 60% 3★, 25% 4★, 15% 5★.
- Pull tickets: `min(5, 1 + pressure // 20 + loop)`.
- Gold: `200 × loop × rand(2.05, 4.25)`.

Rewards are chosen when the foe falls, and the battle scene displays a summary of the loot.

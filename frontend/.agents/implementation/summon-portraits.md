# Summon Portrait Display

Battle snapshots may include `party_summons` and `foe_summons` arrays keyed by `owner_id`.
`BattleView.svelte` now maps these entries to a `summons` property on each fighter.
During combat, each fighter renders any summons beside its portrait:

- Party summons appear to the right of their owner.
- Foe summons appear to the left of their owner.

Summon portraits reuse `FighterPortrait` at 60% of the base `--portrait-size` and respect Reduced Motion settings.
They scale into view using a short Svelte `scale` transition so new summons are noticeable.
When `BattleEffects.svelte` is active, a `SummonSpawn` effect plays the first time a summon appears.

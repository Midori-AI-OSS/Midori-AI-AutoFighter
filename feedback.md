## Feedback Log
Details

### 1) Crafting menu icons missing (In testing)
- Symptom: Crafting list displays item names and counts but icons and star-rank outlines are missing (no visual sprites displayed).
- Impact: Harder to scan materials and identify rarities quickly; reduces UI polish and can confuse players.
- Suggested follow-up: Verify asset paths and rendering logic for crafting items; check CSS rules that may hide background images or SVG icons. Add a fallback placeholder icon when assets fail to load.

### 2) Crafted items do not stack and names are janky (In testing)
- Symptom: Crafted items in the crafting menu do not stack (e.g., 8x 4-star ice items show as 8 separate entries) and names are displayed poorly.
- Impact: Inventory is cluttered and hard to read; user cannot easily see total counts of each item.
- Suggested follow-up: Update UI and logic to stack items by type and rarity, and improve name formatting for clarity.

### 3) Settings UI needs refinement (New issue)
- Symptom: Settings controls are misaligned, labels are inconsistent, and there is no clear save/auto-save affordance.
- Impact: Users are unsure whether changes will be kept; accessibility and layout issues reduce usability.
- Suggested follow-up:
	- Redesign the settings panel for consistent spacing and label placement. Use accessible form controls and visible save state (Saved / Saving / Error).
	- Add autosave with undo and a manual Save button as a fallback. Provide inline validation messages.
	- Run a short UX pass: spacing, font sizes, and keyboard navigation.

### 4) Battle screen missing full stats (New issue)
- Symptom: The battle view does not show the full set of player/foe stats reported by the backend; only a subset (typically HP and basic attack) are visible.
- Impact: Hard to debug combat and tune balance without seeing defense, mitigation, crits, resistances, and advanced metrics in the live battle snapshot.
- Findings (from backend): backend exposes a detailed `player/stats` payload and battle snapshots.
	- Backend source: `backend/app.py` — function `player_stats()` constructs the stats object. Fields to surface in the battle UI include:
		- core: `hp`, `max_hp`, `exp`, `level`, `exp_multiplier`, `actions_per_turn`
		- offense: `atk`, `crit_rate`, `crit_damage`, `effect_hit_rate`, `base_damage_type`
		- defense: `defense`, `mitigation`, `regain`, `dodge_odds`, `effect_resistance`
		- vitality: `vitality`
		- advanced: `action_points`, `damage_taken`, `damage_dealt`, `kills`
		- status: `passives`, `dots`, `hots`, `damage_types`
	- Battle snapshots returned by `/rooms/<run_id>/battle` and the saved `battle_snapshots` are assembled via `_serialize` and the room resolver; confirm `_serialize` includes the above fields for both `party` members and `foes`.
- Suggested follow-up (actionable):
		- Frontend: Update `BattleView.svelte` (or the component rendering the party/foe stat blocks) to display all backend fields. For each stat, add a concise visual:
			- HP / Max HP: progress bar with numeric tooltip (e.g., "48 / 120").
			- ATK: numeric value and small weapon/damage-type icon. Show `base_damage_type` as a colored badge.
			- DEF & Mitigation: show `defense` and a percent-style `mitigation` (e.g., "Mitigation: 24%").
			- Crit Rate / Crit Damage: show as percents ("Crit Rate: 12%", "Crit Damage: +50%") with hover explanation.
			- Regain, Dodge Odds, Effect Resist: show small labeled values (toggleable advanced view to avoid overcrowding).
			- Action Points / Actions Per Turn: show as small counters near portrait.
			- Advanced metrics (damage_dealt, damage_taken, kills): place in a collapsible "Combat stats" section or tooltip for each fighter; useful for post-fight analysis.
			- Status effects: render `hots` and `dots` with stack counts and passive names from `status.passives`.
		- Backend verification: ensure `_serialize` (used when building battle snapshots) returns these fields. If any are missing, add them to the serialized snapshot in `autofighter/` code paths (or expose them from `player`/`foe` models). Files to inspect: `backend/app.py` (battle endpoints), `autofighter/` model serialize helpers (search for `_serialize` implementation) — make sure fields like `crit_rate`, `mitigation`, `effect_resistance`, `action_points`, etc., are included.
		- Tests: Add a small integration test that calls `/rooms/<run_id>/battle?action=snapshot` while a battle is running and asserts the returned `party` and `foes` entries include the keys listed above.

### 5) UI text: "Updating..." should read "Syncing..." during battles (Trivial)
- Symptom: The top-left snapshot panel reads `Updating...` while the battle snapshot is being fetched/updated.
- Impact: The wording is inconsistent with other UI uses of "sync" and can be confusing; "Syncing..." better indicates the round-trip network synchronization in combat.
- Suggested follow-up (actionable):
                - Frontend change: Update `frontend/src/lib/GameViewport.svelte` — change the `<span>Updating...</span>` (snapshot panel) to `<span>Syncing...</span>` so the label matches expected terminology for battle snapshot sync.
                - Also audit any other occurrences of `Updating...` in the UI and change to `Syncing...` where it refers to network synchronization rather than content being edited.

### 6) Loot system follow-up (New issue)
- Symptom: Rare drop rate now multiplies gold rewards, relic odds, upgrade item counts, ticket chances, and—at extreme levels—can roll to raise relic and card star ranks. Future features may not reference it consistently.
- Impact: New rooms or relics could ignore `rdr`, leading to inconsistent loot expectations.
- Suggested follow-up: Document `rdr` usage in future design notes and ensure new content hooks into the existing `gold_earned` event and item-generation helpers.


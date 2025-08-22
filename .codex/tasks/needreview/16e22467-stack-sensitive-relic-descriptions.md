# Stack-Sensitive Relic Descriptions

## Summary
Implement stack-aware relic descriptions across backend and frontend so players see relic effects scaled by the number of stacks they hold.

## Requirements
- [ ] **Backend**
  - Extend `backend/plugins/relics/_base.py` with an `about` field or a `describe(stacks: int) -> str` method returning stack-scaled text.
  - Update each relic plugin in `backend/plugins/relics/` to provide meaningful descriptions or override the new method.
  - In `backend/autofighter/rooms.py`, include both `about` and the current stack count (`party.relics.count(r.id)`) when building `relic_choice_data`.
  - Add tests ensuring relic reward data contains stack-sensitive descriptions.
  - Update docs: link `backend/.codex/implementation/relic-system.md`; add any new relic description notes as needed.
- [ ] **Frontend**
  - In `frontend/src/lib/RewardOverlay.svelte`, render `selected.data.about` for relic rewards.
  - In `frontend/src/lib/RelicInventory.svelte`, show relic descriptions (e.g., tooltip) that automatically respect stack counts.
  - Add tests covering rendering of stack-sensitive descriptions.
  - Update docs: link `.codex/implementation/relic-inventory.md`, `.codex/implementation/reward-overlay.md`.
- [ ] **Docs & Tasks**
  - Sync any new documentation in appropriate `*/.codex/implementation` files.
  - Ensure commit references this task file.

## Testing
- `uv run pytest` (backend)
- `bun test` (frontend)
- `uvx ruff check backend`
- `ESLINT_USE_FLAT_CONFIG=false bunx eslint .`

## References
- `.codex/implementation/relic-system.md`
- `.codex/implementation/relic-inventory.md`
- `.codex/implementation/reward-overlay.md`
- `.codex/planning/bd48a561-relic-plan.md`
- `feedback.md` (context on current UI)

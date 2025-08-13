# Build gacha character recruitment

## Summary
Implemented a simple `GachaManager` that tracks pity, upgrade items, and
character stacks in the encrypted save. Quart exposes `GET /gacha` and
`POST /gacha/pull` for performing 1, 5, or 10 pulls and returning updated
gacha state. New characters are added to `owned_players` immediately so they
can join the party during rest rooms.

## Acceptance Criteria
- Pulling returns characters or upgrade items according to plan odds.
- Tests cover pity progression, duplicate handling, and rest-node pulls sharing
  the same pity state.

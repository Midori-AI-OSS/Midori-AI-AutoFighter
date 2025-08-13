# Build gacha character recruitment
Allow players to spend upgrade items on gacha pulls for new characters. Parent: [Gacha Character Recruitment Plan](../planning/82dc97b7-gacha-character-recruitment-plan.md).

## Requirements
- Implement `GachaManager` with pity counters, roll tables, and batch pull options.
- Serialize upgrade items, character stacks, and pity state in saves.
- Provide endpoints for performing pulls and listing owned characters.

## Acceptance Criteria
- Pulling returns characters or upgrade items according to plan odds.
- Tests cover pity progression and duplicate handling.

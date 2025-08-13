# Build gacha character recruitment
Allow players to spend upgrade items on gacha pulls for new characters. Parent: [Gacha Character Recruitment Plan](../planning/82dc97b7-gacha-character-recruitment-plan.md).

## Requirements
- Implement `GachaManager` with pity counters, roll tables, and batch pull options.
- Serialize upgrade items, character stacks, and pity state in saves.
- Provide endpoints for performing pulls and listing owned characters that are accessible outside of runs and during rest nodes.
- Rest-node pulls share pity counters and currency with main-menu pulls and let players pull repeatedly before moving on.
- Make new characters from rest-node pulls immediately available to join the party during that rest.

## Acceptance Criteria
- Pulling returns characters or upgrade items according to plan odds.
- Tests cover pity progression, duplicate handling, and rest-node pulls sharing the same pity state.

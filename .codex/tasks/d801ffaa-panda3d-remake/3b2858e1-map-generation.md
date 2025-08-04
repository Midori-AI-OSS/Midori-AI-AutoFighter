# Map Generation System

## Summary
Implement the run map with room nodes, links, and seeded randomization.

## Tasks
- [ ] Generate 45-room floors containing rest, chat, battle-weak, battle-normal, battle-boss, battle-boss-floor, and shop nodes.
- [ ] Ensure each floor has at least two shops and two rest stops; chats occur after fights without consuming room count.
- [ ] Support Pressure Level selection that scales foes and adds rooms or bosses at specified intervals.
- [ ] Loop maps endlessly after the final floor with enemy scaling per loop.
- [ ] Render a color-coded vertical map showing room connections, current location, and valid paths.
- [ ] Seed each floor from a run-specific base seed and forbid seed reuse.

## Context
The map guides progression and needs deterministic generation for testing.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.

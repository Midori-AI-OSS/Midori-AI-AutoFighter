# Build map generator and room types
Create 45-room floors with shops, rests, battles, chats, and boss nodes. Parent: [Map and Room Types Plan](../planning/e158df1a-map-and-room-types-plan.md).

> Review the Pressure Level rules in the plan before implementing scaling.

## Requirements
- Implement `MapGenerator` and `MapNode` dataclass with deterministic seeding.
- Add `Room` subclasses for battle, rest, shop, chat, and boss behaviors.
- Scale foes and rewards by floor, room level, loop, and Pressure settings.

## Acceptance Criteria
- Generated maps honor room quotas and Pressure adjustments.
- Endpoints can transition between generated rooms and return appropriate rewards.

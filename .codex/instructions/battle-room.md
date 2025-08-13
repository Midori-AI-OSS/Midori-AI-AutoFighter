# Battle Room

Describes the backend battle endpoint.

- Exchanges event-bus-driven attacks, comparing player attack against foe defense.
- Foe stats scale with floor, room, Pressure level, and loop count.
- Returns damage numbers, attack effects, and status icons for the frontend to render.
- Each turn increments a counter; after 100 turns (500 for floor bosses) an overtime warning triggers and grants foes a 40% attack buff.
- Exiting returns control to the previous room.

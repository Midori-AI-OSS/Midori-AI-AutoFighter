# Battle Room

Describes the battle scene.

- Renders placeholder cube models for player and foe using Panda3D node graphs.
- Attacks trigger through messenger events and compare player attack against foe defense.
- Foe stats scale with floor, room, Pressure level, and loop count.
- Damage flashes targets, spawns floating numbers, draws simple attack effects, and adds status icons.
- Each turn increments a counter; after 100 turns (500 for floor bosses) an overtime warning appears, the room flashes red and blue, and an "Enraged" icon grants foes a 40% attack buff.
- Escape returns to the previous scene.

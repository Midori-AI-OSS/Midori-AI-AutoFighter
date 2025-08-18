# Battle Room

Describes the backend battle endpoint.

- Exchanges event-bus-driven attacks, comparing player attack against foe defense.
- Foe stats scale with floor, room, Pressure level, and loop count.
- Returns damage numbers, attack effects, and status icons for the frontend to render.
- Each turn increments a counter; after 100 turns (500 for floor bosses) an overtime warning triggers. Foes gain a 40% `Enraged` attack buff every subsequent turn, stacking endlessly, and the battle background cycles between blue and red roughly every ten seconds while enrage is active. The animation slows further when the **Reduced Motion** option is enabled.
- Exiting returns control to the previous room.
- The top navigation bar remains visible during battles, with the home button replaced by a non-interactive battle icon.
- The reward overlay centers on the battle viewport and sizes to a 1×3 card grid, expanding to 2×3 when six cards are offered.
- Combat UI places the party in a resizable left column with stats beside each portrait and HoT/DoT markers below; foes mirror the layout on the right.
- The frontend polls `roomAction(runId, 'battle', 'snapshot')` at an interval derived from the frame-rate setting to fetch full party and foe snapshots without overloading the CPU.

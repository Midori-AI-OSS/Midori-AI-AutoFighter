# Battle View

`BattleView.svelte` renders turn-based encounters inside `MenuPanel` and now
acts primarily as a coordinator. It draws a random backdrop from the shared
`assetLoader` and displays the party and foes in opposing columns, with the
party fixed to the left and foes to the right using explicit flex order.

Visual pieces have been split into small subcomponents under
`src/lib/battle/`:

- `FighterPortrait.svelte` – portrait, HP bar, element chip (circular dark
  backdrop with a strong background blur; no outer glow) and embedded
  `StatusIcons`. Passive stack pips render as vector icons and tint to the
  element color when filled. Portrait resolution prefers `fighter.summon_type`
  when present so summons can reuse shared art folders.
- `StatusIcons.svelte` – collapses duplicate HoT/DoT names into single icons
  with stack counts.
- `EnrageIndicator.svelte` – pulsing red/blue overlay when the backend reports
  `enrage.active`.
- `BattleLog.svelte` – lightweight scrollable list fed with log messages from
  snapshots.

Each combatant lists HP, ATK, DEF, mitigation, and crit rate beside their
portrait, mirroring the same order for party and foes. Shared fallback art
appears when portraits are missing, and the layout scales down on small screens
so both the bars and numeric values remain readable.

### Pips (Passive Stacks)

Fighter passive stacks are displayed as small, colorable pips near the bottom‑right
of the portrait, just to the left of the element chip.

- Rendering:
  - For passives with `max_stacks <= 5`, show up to 5 circular pips.
  - The number of filled pips equals `stacks` (clamped to `max_stacks`).
  - Filled pips use the fighter’s element color; empty pips are neutral.
  - For `max_stacks > 5`, show a compact numeric label `stacks/max` instead of pips.
- Implementation:
  - Uses `lucide-svelte` Circle as the pip glyph; styled via `currentColor`.
  - The pip container removes the usual glass background to avoid a dark bar,
    sets `line-height: 0`, and the pip icon uses `display: block` for clean alignment.
  - Reduced motion disables any transition effects.
- Sizing and layout:
  - Pips scale with portrait size using CSS vars in `FighterPortrait.svelte`:
    - `--pip-size: clamp(4px, calc(var(--portrait-size) * 0.11), 10px)`
    - `--pip-gap: clamp(1px, calc(var(--portrait-size) * 0.02), 3px)`
  - The element chip size also scales with `--portrait-size`, maintaining spacing
    between the pips and the chip across views (Battle View, Review, tabs).

Accessibility: Each passive has a `title`/`aria-label` that includes its id and
stack info (for example, `id 3/5`).

Snapshots from the backend are polled once per frame-rate tick rather than on a
fixed interval and the polling delay honors 30/60/120 fps settings without a
50 ms floor. Each request dispatches events with the round-trip time so
`NavBar` shows a stained-glass status panel with a
spinner while updates are in flight. Incoming party and foe arrays are compared
to the previous snapshot to avoid unnecessary re-renders.

Summon data is provided through `party_summons` and `foe_summons` objects keyed
by the summoner's id. The view flattens these maps into arrays grouped by owner
so that summoned units render alongside their summoners.

## Testing
- `bun test frontend/tests/battleview.test.js`

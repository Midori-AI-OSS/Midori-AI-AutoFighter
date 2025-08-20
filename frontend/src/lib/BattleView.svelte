<script>
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import { roomAction } from './api.js';
  import { getCharacterImage, getRandomBackground, getElementColor, getElementIcon } from './assetLoader.js';
  export let runId = '';
  export let framerate = 60;
  export let party = [];
  export let enrage = { active: false, stacks: 0 };
  export let reducedMotion = false;
  let foes = [];
  let timer;
  const dispatch = createEventDispatcher();
  let pollDelay = 1000 / framerate;
  $: pollDelay = 1000 / framerate;
  let bg = getRandomBackground();
  $: flashDuration = reducedMotion ? 20 : 10;

  function differs(a, b) {
    return JSON.stringify(a) !== JSON.stringify(b);
  }

  function groupEffects(list) {
    const counts = {};
    for (const e of list || []) counts[e] = (counts[e] || 0) + 1;
    return Object.entries(counts);
  }

  function pctRatio(val) {
    if (typeof val !== 'number' || !isFinite(val)) return '0%';
    return `${Math.round(val * 100)}%`;
  }

  function pctOdds(val) {
    if (typeof val !== 'number' || !isFinite(val)) return '0%';
    return `${Math.round(val * 100)}%`;
  }

  function pctFromMultiplier(mult) {
    if (typeof mult !== 'number' || !isFinite(mult)) return '0%';
    return `${Math.round((mult - 1) * 100)}%`;
  }

  function formatMitigation(val) {
    if (typeof val !== 'number' || !isFinite(val)) return '-';
    // Rule: 100 = 1x (no mitigation). <100 means more damage taken, >100 reduces damage.
    if (val >= 10) {
      return `x${(val / 100).toFixed(2)}`;
    }
    // If value is already a small multiplier (e.g., 1.0), show directly.
    return `x${val.toFixed(2)}`;
  }

  function guessElementFromId(id) {
    const s = (id || '').toLowerCase();
    if (s.includes('lightning')) return 'Lightning';
    if (s.includes('light')) return 'Light';
    if (s.includes('dark')) return 'Dark';
    if (s.includes('fire')) return 'Fire';
    if (s.includes('ice')) return 'Ice';
    if (s.includes('wind')) return 'Wind';
    return 'Generic';
  }

  function elementOf(obj) {
    // Prefer explicit element alias if present
    const elem = obj?.element;
    if (typeof elem === 'string' && elem.length) return elem;
    // Fallback to base_damage_type
    const dt = obj?.base_damage_type;
    if (!dt) return guessElementFromId(obj?.id);
    if (typeof dt === 'string' && dt.length) return dt;
    return dt.id || dt.name || guessElementFromId(obj?.id);
  }

  async function fetchSnapshot() {
    const start = performance.now();
    dispatch('snapshot-start');
    try {
      const snap = await roomAction(runId, 'battle', 'snapshot');
      if (snap.party && differs(snap.party, party)) party = snap.party;
      if (snap.foes && differs(snap.foes, foes)) foes = snap.foes;
      if (snap.enrage && differs(snap.enrage, enrage)) enrage = snap.enrage;
      if (snap.party) {
        const prevById = new Map((party || []).map(p => [p.id, p]));
        const enriched = (snap.party || []).map(m => {
          let elem = m.element || m.base_damage_type || '';
          if (!elem || /generic/i.test(String(elem))) {
            const prev = prevById.get(m.id);
            if (prev && (prev.element || prev.base_damage_type)) {
              elem = prev.element || prev.base_damage_type;
            } else {
              elem = guessElementFromId(m.id);
            }
          }
          const resolved = typeof elem === 'string' ? elem : (elem?.id || elem?.name || 'Generic');
          return { ...m, element: resolved };
        });
        if (differs(enriched, party)) party = enriched;
      }
      if (snap.foes) {
        const prevById = new Map((foes || []).map(f => [f.id, f]));
        const enrichedFoes = (snap.foes || []).map(f => {
          let elem = f.element || f.base_damage_type || '';
          if (!elem || /generic/i.test(String(elem))) {
            const prev = prevById.get(f.id);
            if (prev && (prev.element || prev.base_damage_type)) {
              elem = prev.element || prev.base_damage_type;
            } else {
              elem = guessElementFromId(f.id);
            }
          }
          const resolved = typeof elem === 'string' ? elem : (elem?.id || elem?.name || 'Generic');
          return { ...f, element: resolved };
        });
        if (differs(enrichedFoes, foes)) foes = enrichedFoes;
      }
    } catch (e) {
      /* ignore */
    } finally {
      const duration = performance.now() - start;
      dispatch('snapshot-end', { duration });
      console.log(`snapshot ${duration.toFixed(1)}ms`);
      timer = setTimeout(fetchSnapshot, Math.max(0, pollDelay - duration));
    }
  }

  onMount(() => {
    fetchSnapshot();
  });

  onDestroy(() => {
    clearTimeout(timer);
  });
</script>

<div
  class="battle-field"
  class:enraged={enrage?.active}
  style={`background-image: url(${bg}); --flash-duration: ${flashDuration}s`}
  data-testid="battle-view"
>
  <div class="party-column">
    {#each party as member (member.id)}
      <div class="combatant">
        <div class="portrait-wrap">
          <div class="hp-bar">
            <div
              class="hp-fill"
              style={`width: ${member.max_hp ? (100 * member.hp) / member.max_hp : 0}%`}
            ></div>
          </div>
          <div class="portrait-frame">
            <img
              src={getCharacterImage(member.id, true)}
              alt=""
              class="portrait"
              style={`border-color: ${getElementColor(elementOf(member))}`}
            />
            <div class="element-chip">
              <svelte:component
                this={getElementIcon(elementOf(member))}
                class="element-icon"
                style={`color: ${getElementColor(elementOf(member))}`}
                aria-hidden="true" />
            </div>
          </div>
          <div class="effects">
            {#each groupEffects(member.hots) as [name, count]}
              <span class="hot" title={name}>
                {#if count > 1}<span class="stack">{count}</span>{/if}
              </span>
            {/each}
            {#each groupEffects(member.dots) as [name, count]}
              <span class="dot" title={name}>
                {#if count > 1}<span class="stack">{count}</span>{/if}
              </span>
            {/each}
          </div>
        </div>
        <div class="stats right">
          <div class="row"><span class="k">HP</span> <span class="v">{member.hp}/{member.max_hp}</span></div>
          <div class="row"><span class="k">ATK</span> <span class="v">{member.atk}</span></div>
          <div class="row"><span class="k">DEF</span> <span class="v">{member.defense}</span></div>
          <div class="row"><span class="k">MIT</span> <span class="v">{formatMitigation(member.mitigation)}</span></div>
          <div class="row"><span class="k">CRate</span> <span class="v">{pctOdds(member.crit_rate)}</span></div>
          <div class="row"><span class="k">CDmg</span> <span class="v">{pctFromMultiplier(member.crit_damage)}</span></div>
          <div class="row"><span class="k">E.Hit</span> <span class="v">{pctRatio(member.effect_hit_rate)}</span></div>
          <div class="row"><span class="k">E.Res</span> <span class="v">{pctOdds(member.effect_resistance)}</span></div>
          <div class="row small"><span class="k">AP</span> <span class="v">{member.action_points ?? 0}</span> <span class="k">/ APT</span> <span class="v">{member.actions_per_turn ?? 1}</span></div>
          <details class="advanced">
            <summary>Combat stats</summary>
            <div class="row small"><span class="k">Dmg Dealt</span> <span class="v">{member.damage_dealt ?? 0}</span></div>
            <div class="row small"><span class="k">Dmg Taken</span> <span class="v">{member.damage_taken ?? 0}</span></div>
            <div class="row small"><span class="k">Kills</span> <span class="v">{member.kills ?? 0}</span></div>
          </details>
        </div>
      </div>
    {/each}
  </div>
  <div class="foe-column">
    {#each foes as foe (foe.id)}
      <div class="combatant">
        <div class="stats left">
          <div class="row"><span class="k">HP</span> <span class="v">{foe.hp}/{foe.max_hp}</span></div>
          <div class="row"><span class="k">ATK</span> <span class="v">{foe.atk}</span></div>
          <div class="row"><span class="k">DEF</span> <span class="v">{foe.defense}</span></div>
          <div class="row"><span class="k">MIT</span> <span class="v">{formatMitigation(foe.mitigation)}</span></div>
          <div class="row"><span class="k">CRate</span> <span class="v">{pctOdds(foe.crit_rate)}</span></div>
          <div class="row"><span class="k">CDmg</span> <span class="v">{pctFromMultiplier(foe.crit_damage)}</span></div>
          <div class="row"><span class="k">E.Hit</span> <span class="v">{pctRatio(foe.effect_hit_rate)}</span></div>
          <div class="row"><span class="k">E.Res</span> <span class="v">{pctOdds(foe.effect_resistance)}</span></div>
          <div class="row small"><span class="k">AP</span> <span class="v">{foe.action_points ?? 0}</span> <span class="k">/ APT</span> <span class="v">{foe.actions_per_turn ?? 1}</span></div>
        <details class="advanced">
            <summary>Combat stats</summary>
            <div class="row small"><span class="k">Dmg Dealt</span> <span class="v">{foe.damage_dealt ?? 0}</span></div>
            <div class="row small"><span class="k">Dmg Taken</span> <span class="v">{foe.damage_taken ?? 0}</span></div>
            <div class="row small"><span class="k">Kills</span> <span class="v">{foe.kills ?? 0}</span></div>
          </details>
        </div>
        <div class="portrait-wrap">
          <div class="hp-bar">
            <div
              class="hp-fill"
              style={`width: ${foe.max_hp ? (100 * foe.hp) / foe.max_hp : 0}%`}
            ></div>
          </div>
          <div class="portrait-frame">
            <img
              src={getCharacterImage(foe.id)}
              alt=""
              class="portrait"
              style={`border-color: ${getElementColor(elementOf(foe))}`}
            />
            <div class="element-chip">
              <svelte:component
                this={getElementIcon(elementOf(foe))}
                class="element-icon"
                style={`color: ${getElementColor(elementOf(foe))}`}
                aria-hidden="true" />
            </div>
          </div>
          <div class="effects">
            {#each groupEffects(foe.hots) as [name, count]}
              <span class="hot" title={name}>
                {#if count > 1}<span class="stack">{count}</span>{/if}
              </span>
            {/each}
            {#each groupEffects(foe.dots) as [name, count]}
              <span class="dot" title={name}>
                {#if count > 1}<span class="stack">{count}</span>{/if}
              </span>
            {/each}
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .battle-field {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 0.5rem;
    overflow: hidden;
  }
  .battle-field.enraged::after {
    content: '';
    position: absolute;
    inset: 0;
    z-index: 0;
    animation: enrage-bg var(--flash-duration) linear infinite;
  }
  .battle-field > * {
    position: relative;
    z-index: 1;
  }
  @keyframes enrage-bg {
    0%,100% { background: rgba(0,0,255,0.4); }
    50% { background: rgba(255,0,0,0.4); }
  }
  .party-column,
  .foe-column {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.5rem;
  }

  .party-column {
    order: 1;
  }

  .foe-column {
    order: 2;
  }
  .combatant {
    display: flex;
    align-items: center;
  }
  .foe-column .combatant {
    flex-direction: row-reverse;
  }
  .portrait-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .hp-bar {
    width: 6rem;
    height: 0.5rem;
    border: 1px solid #000;
    background: #333;
    margin-bottom: 0.2rem;
  }
  .hp-fill {
    height: 100%;
    background: #0f0;
  }
  .portrait-frame { position: relative; width: 6rem; height: 6rem; }
  .portrait {
    width: 100%;
    height: 100%;
    border: 2px solid #555;
    border-radius: 4px;
    display: block;
  }
  .element-chip { position: absolute; bottom: 2px; right: 2px; z-index: 2; display: flex; align-items: center; justify-content: center; pointer-events: none; }
  .element-icon { width: 16px; height: 16px; display: block; }
  .stats {
    font-size: 0.7rem;
    width: 6rem;
  }
  .row { display: flex; justify-content: space-between; gap: 0.25rem; }
  .row.small { font-size: 0.65rem; }
  .k { opacity: 0.85; }
  .v { font-variant-numeric: tabular-nums; }
  .badge { display: none; }
  details.advanced { margin-top: 0.15rem; }
  .stats.right {
    margin-left: 0.25rem;
    text-align: left;
  }
  .stats.left {
    margin-right: 0.25rem;
    text-align: right;
  }
  .effects {
    display: flex;
    gap: 0.2rem;
    margin-top: 0.15rem;
  }
  .effects span {
    position: relative;
  }
  .hot,
  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
  }
  .hot { background: #0f0; }
  .dot { background: #f00; }
  .stack {
    position: absolute;
    bottom: -2px;
    right: -2px;
    font-size: 0.5rem;
  }

  @media (max-width: 600px) {
    .hp-bar {
      width: 4rem;
    }
    .portrait {
      width: 4rem;
      height: 4rem;
    }
    .stats {
      width: 4rem;
      font-size: 0.6rem;
    }
  }
</style>

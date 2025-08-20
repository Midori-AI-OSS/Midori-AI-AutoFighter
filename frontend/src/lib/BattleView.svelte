<script>
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import { roomAction } from './api.js';
  import { getCharacterImage, getRandomBackground } from './assetLoader.js';
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

  async function fetchSnapshot() {
    const start = performance.now();
    dispatch('snapshot-start');
    try {
      const snap = await roomAction(runId, 'battle', 'snapshot');
      if (snap.party && differs(snap.party, party)) party = snap.party;
      if (snap.foes && differs(snap.foes, foes)) foes = snap.foes;
      if (snap.enrage && differs(snap.enrage, enrage)) enrage = snap.enrage;
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
          <img src={getCharacterImage(member.id, true)} alt="" class="portrait" />
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
          <div>HP {member.hp}/{member.max_hp}</div>
          <div>ATK {member.atk}</div>
          <div>DEF {member.defense}</div>
          <div>MIT {member.mitigation}</div>
          <div>CRIT {(member.crit_rate * 100).toFixed(0)}%</div>
        </div>
      </div>
    {/each}
  </div>
  <div class="foe-column">
    {#each foes as foe (foe.id)}
      <div class="combatant">
        <div class="stats left">
          <div>HP {foe.hp}/{foe.max_hp}</div>
          <div>ATK {foe.atk}</div>
          <div>DEF {foe.defense}</div>
          <div>MIT {foe.mitigation}</div>
          <div>CRIT {(foe.crit_rate * 100).toFixed(0)}%</div>
        </div>
        <div class="portrait-wrap">
          <div class="hp-bar">
            <div
              class="hp-fill"
              style={`width: ${foe.max_hp ? (100 * foe.hp) / foe.max_hp : 0}%`}
            ></div>
          </div>
          <img src={getCharacterImage(foe.id)} alt="" class="portrait" />
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
  .portrait {
    width: 6rem;
    height: 6rem;
    border: 2px solid #555;
    border-radius: 4px;
  }
  .stats {
    font-size: 0.7rem;
    width: 6rem;
  }
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

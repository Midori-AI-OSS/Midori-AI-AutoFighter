<script>
  import { onMount, onDestroy } from 'svelte';
  import { roomAction } from './api.js';
  import { getCharacterImage, getRandomBackground } from './assetLoader.js';
  export let runId = '';
  export let framerate = 60;
  export let party = [];
  export let enrage = { active: false, stacks: 0 };
  export let reducedMotion = false;
  let foes = [];
  let timer;
  let bg = getRandomBackground();
  $: flashDuration = reducedMotion ? 20 : 10;

  async function fetchSnapshot() {
    try {
      const snap = await roomAction(runId, 'battle', 'snapshot');
      if (snap.party) party = snap.party;
      if (snap.foes) foes = snap.foes;
    } catch (e) {
      /* ignore */
    }
  }

  onMount(() => {
    fetchSnapshot();
    const delay = 1000 / framerate;
    timer = setInterval(fetchSnapshot, delay);
  });

  onDestroy(() => {
    clearInterval(timer);
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
          <img src={getCharacterImage(member.id, true)} alt="" class="portrait" />
          <div class="effects">
            {#each member.hots || [] as h}
              <span class="hot" title={h}></span>
            {/each}
            {#each member.dots || [] as d}
              <span class="dot" title={d}></span>
            {/each}
          </div>
        </div>
        <div class="stats right">
          <div>HP {member.hp}/{member.max_hp}</div>
          <div>ATK {member.atk}</div>
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
        </div>
        <div class="portrait-wrap">
          <img src={getCharacterImage(foe.id)} alt="" class="portrait" />
          <div class="effects">
            {#each foe.hots || [] as h}
              <span class="hot" title={h}></span>
            {/each}
            {#each foe.dots || [] as d}
              <span class="dot" title={d}></span>
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
  .portrait {
    width: 48px;
    height: 48px;
    border: 2px solid #555;
    border-radius: 4px;
  }
  .stats {
    font-size: 0.7rem;
    width: 4.5rem;
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
  .hot,
  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
  }
  .hot { background: #0f0; }
  .dot { background: #f00; }
</style>

<script>
  import { createEventDispatcher } from 'svelte';
  import { cardArt, getRewardArt, randomCardArt } from './rewardLoader.js';

  const starColors = {
    1: '#808080',
    2: '#228B22',
    3: '#1E90FF',
    4: '#800080',
    5: '#FFD700',
    fallback: '#708090'
  };

  export let cards = [];
  export let relics = [];
  export let items = [];
  export let gold = 0;

  const dispatch = createEventDispatcher();
  const artMap = new Map();

  function artFor(card) {
    if (!artMap.has(card.id)) {
      if (cardArt[card.id]) {
        artMap.set(card.id, getRewardArt('card', card.id));
      } else {
        artMap.set(card.id, randomCardArt());
      }
    }
    return artMap.get(card.id);
  }

  function titleForItem(item) {
    if (!item) return '';
    if (item.name) return item.name;
    if (item.id === 'ticket') return 'Gacha Ticket';
    const id = String(item.id || '').toLowerCase();
    const cap = id.charAt(0).toUpperCase() + id.slice(1);
    const stars = Number.isFinite(item.stars) ? `${item.stars}★` : '';
    return stars ? `${cap} Upgrade (${stars})` : `${cap} Upgrade`;
  }

  let selected = null;
  $: remaining = cards.length + relics.length;

  function show(type, entry) {
    selected = { type, data: entry };
  }

  function confirm() {
    if (selected) {
      dispatch('select', { type: selected.type, id: selected.data.id });
      selected = null;
    }
  }
</script>

<style>
  .reward {
    margin: auto;
    width: fit-content;
    height: fit-content;
  }

  .choices {
    display: grid;
    grid-template-columns: repeat(3, 72px);
    grid-auto-rows: 96px;
    gap: 0.5rem;
    justify-content: center;
  }
  .choice {
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    color: #fff;
  }
  .art {
    position: relative;
    width: 72px;
    height: 96px;
    background: transparent;
    overflow: hidden;
  }
  .art img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    filter: grayscale(1);
  }
  .label {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.55);
    font-size: 0.7rem;
    text-align: center;
    padding: 1px 2px;
    line-height: 1.1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .status {
    margin-top: 0.5rem;
    text-align: center;
  }
</style>

<div class="reward">
  {#if cards.length}
    <h3>Choose a Card</h3>
    <div class="choices">
      {#each cards as card}
        <button
          class="choice"
          on:click={() => show('card', card)}
        >
          <div
            class="art"
            style={`--star-color: ${starColors[card.stars] || starColors.fallback}`}
          >
            <img src={artFor(card)} alt={card.name} />
            <div class="label">{card.name}</div>
          </div>
        </button>
      {/each}
    </div>
  {/if}
  {#if relics.length}
    <h3>Choose a Relic</h3>
    <div class="choices">
      {#each relics as relic}
        <button class="choice" on:click={() => show('relic', relic)}>
          <div
            class="art"
            style={`--star-color: ${starColors[relic.stars] || starColors.fallback}`}
          >
            <img src={getRewardArt('relic', relic.id)} alt={relic.name} />
            <div class="label">{relic.name}</div>
          </div>
        </button>
      {/each}
    </div>
  {/if}
  {#if items.length}
    <h3>Drops</h3>
    <div class="status">
      <ul>
        {#each items as item}
          <li>{titleForItem(item)}</li>
        {/each}
      </ul>
    </div>
  {/if}
  {#if selected}
    <div class="status">
      <strong>{selected.data.name}</strong>
      {#if selected.type === 'card'}
        <p>{selected.data.about}</p>
      {/if}
      <button on:click={confirm}>Confirm</button>
    </div>
  {/if}
  {#if gold}
    <div class="status">Gold +{gold}</div>
  {/if}
  <div class="status">
    <button on:click={() => dispatch('next')} disabled={remaining > 0}>Next Room</button>
  </div>
</div>

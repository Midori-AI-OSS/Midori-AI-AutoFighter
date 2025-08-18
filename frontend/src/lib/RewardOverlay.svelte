<script>
  import { createEventDispatcher } from 'svelte';
  import { cardArt, getRewardArt, randomCardArt } from './rewardLoader.js';
  import MenuPanel from './MenuPanel.svelte';

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

  let selected = null;

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

  .reward :global(.panel) {
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
    background-color: var(--star-color, #708090);
  }
  .art img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: grayscale(1);
    mix-blend-mode: multiply;
  }
  .label {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.5);
    font-size: 0.7rem;
    text-align: center;
  }
  .status {
    margin-top: 0.5rem;
    text-align: center;
  }
</style>

<div class="reward">
<MenuPanel>
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
          <div class="art" style="--star-color: #708090">
            {#if getRewardArt('relic', relic.id)}
              <img src={getRewardArt('relic', relic.id)} alt={relic.name} />
            {/if}
            <div class="label">{relic.name}</div>
          </div>
        </button>
      {/each}
    </div>
  {/if}
  {#if items.length}
    <h3>Choose an Item</h3>
    <div class="choices">
      {#each items as item}
        <button class="choice" on:click={() => show('item', item)}>
          <div class="art" style="--star-color: #708090">
            {#if getRewardArt('item', item.id)}
              <img src={getRewardArt('item', item.id)} alt={item.name} />
            {/if}
            <div class="label">{item.name}</div>
          </div>
        </button>
      {/each}
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
</MenuPanel>
</div>

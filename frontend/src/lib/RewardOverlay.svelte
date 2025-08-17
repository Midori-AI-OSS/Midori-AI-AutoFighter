<script>
  import { createEventDispatcher } from 'svelte';
  import { getRewardArt } from './rewardLoader.js';
  import MenuPanel from './MenuPanel.svelte';
  export let cards = [];
  export let relics = [];
  export let items = [];
  const dispatch = createEventDispatcher();
  function select(type, id) {
    dispatch('select', { type, id });
  }
</script>

<style>
  .choices {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
  }
  .choice {
    background: none;
    border: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    color: #fff;
  }
  .choice img {
    width: 72px;
    height: 96px;
    object-fit: contain;
    margin-bottom: 0.25rem;
  }
</style>

<MenuPanel>
  {#if cards.length}
    <h3>Choose a Card</h3>
    <div class="choices">
      {#each cards as card}
        <button class="choice" on:click={() => select('card', card.id)}>
          {#if getRewardArt('card', card.id)}
            <img src={getRewardArt('card', card.id)} alt={card.name} />
          {/if}
          <span>{card.name}</span>
        </button>
      {/each}
    </div>
  {/if}
  {#if relics.length}
    <h3>Choose a Relic</h3>
    <div class="choices">
      {#each relics as relic}
        <button class="choice" on:click={() => select('relic', relic.id)}>
          {#if getRewardArt('relic', relic.id)}
            <img src={getRewardArt('relic', relic.id)} alt={relic.name} />
          {/if}
          <span>{relic.name}</span>
        </button>
      {/each}
    </div>
  {/if}
  {#if items.length}
    <h3>Choose an Item</h3>
    <div class="choices">
      {#each items as item}
        <button class="choice" on:click={() => select('item', item.id)}>
          {#if getRewardArt('item', item.id)}
            <img src={getRewardArt('item', item.id)} alt={item.name} />
          {/if}
          <span>{item.name}</span>
        </button>
      {/each}
    </div>
  {/if}
</MenuPanel>

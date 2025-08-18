<script>
  import MenuPanel from './MenuPanel.svelte';
  import { Coins } from 'lucide-svelte';
  import { createEventDispatcher } from 'svelte';
  export let items = [];
  export let gold = 0;
  export let reducedMotion = false;
  const dispatch = createEventDispatcher();
  function buy(item) { dispatch('buy', item); }
  function reroll() { dispatch('reroll'); }
  function close() { dispatch('close'); }
</script>

<MenuPanel data-testid="shop-menu">
  <h3>Shop</h3>
  <p class="currency"><Coins size={16} class="coin-icon" class:shine={!reducedMotion} /> {gold}</p>
  <ul class="items">
    {#each items as item}
      <li>
        <span>{item.name} - {(item.price ?? item.cost ?? 0)}</span>
        <button on:click={() => buy(item)}>Buy</button>
      </li>
    {/each}
  </ul>
  <div class="actions">
    <button on:click={reroll}>Reroll</button>
    <button on:click={close}>Leave</button>
  </div>
</MenuPanel>

<style>
  .items {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  li {
    display: flex;
    justify-content: space-between;
    border: 2px solid #fff;
    padding: 0.25rem 0.5rem;
    background: #111;
    color: #fff;
  }
  .actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }
  button {
    border: 2px solid #fff;
    background: #0a0a0a;
    color: #fff;
    padding: 0.3rem 0.6rem;
  }
  .currency {
    margin: 0 0 0.5rem 0;
    text-align: center;
  }
  .coin-icon {
    color: #d4af37;
  }
  .shine {
    animation: coin-shine 2s linear infinite;
  }
  @keyframes coin-shine {
    0%,100% { filter: brightness(1); }
    50% { filter: brightness(1.4); }
  }
</style>

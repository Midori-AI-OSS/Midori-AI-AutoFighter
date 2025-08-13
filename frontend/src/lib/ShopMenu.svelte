<script>
  import MenuPanel from './MenuPanel.svelte';
  import { createEventDispatcher } from 'svelte';
  export let items = [];
  const dispatch = createEventDispatcher();
  function buy(item) { dispatch('buy', item); }
  function reroll() { dispatch('reroll'); }
  function close() { dispatch('close'); }
</script>

<MenuPanel data-testid="shop-menu">
  <h3>Shop</h3>
  <ul class="items">
    {#each items as item}
      <li>
        <span>{item.name}</span>
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
</style>

<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import MenuPanel from './MenuPanel.svelte';
  import { getGacha, pullGacha } from './api.js';
  const dispatch = createEventDispatcher();
  let pity = 0;
  let items = {};
  let results = [];
  let loading = false;
  onMount(async () => {
    const data = await getGacha();
    pity = data.pity;
    items = data.items;
  });
  async function pull(count) {
    loading = true;
    const data = await pullGacha(count);
    pity = data.pity;
    items = data.items;
    results = data.results || [];
    loading = false;
  }
  function close() {
    dispatch('close');
  }
</script>

<MenuPanel data-testid="pulls-menu">
  <h3>Pulls</h3>
  <p>Pity: {pity}</p>
  <p>Tickets: {items.ticket || 0}</p>
  <div class="actions">
    <button disabled={loading} on:click={() => pull(1)}>Pull 1</button>
    <button disabled={loading} on:click={() => pull(10)}>Pull 10</button>
    <button on:click={close}>Done</button>
  </div>
  {#if results.length}
    <ul>
      {#each results as r}
        <li>{r.type}: {r.id} ({r.rarity}★){#if r.stacks} x{r.stacks}{/if}</li>
      {/each}
    </ul>
  {/if}
</MenuPanel>

<style>
  .actions {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  button {
    border: 2px solid #fff;
    background: #0a0a0a;
    color: #fff;
    padding: 0.3rem 0.6rem;
  }
  ul {
    margin: 0;
    padding-left: 1rem;
  }
</style>

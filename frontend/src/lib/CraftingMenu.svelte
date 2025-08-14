<script>
  import MenuPanel from './MenuPanel.svelte';
  import { createEventDispatcher, onMount } from 'svelte';
  import { getGacha, setAutoCraft, craftItems } from './api.js';

  const dispatch = createEventDispatcher();
  let items = {};
  let autoCraft = false;

  onMount(async () => {
    const state = await getGacha();
    items = state.items || {};
    autoCraft = state.auto_craft || false;
  });

  async function craft() {
    const res = await craftItems();
    items = res.items || {};
  }

  async function toggleAuto() {
    autoCraft = !autoCraft;
    await setAutoCraft(autoCraft);
  }

  function close() {
    dispatch('close');
  }
</script>

<MenuPanel data-testid="crafting-menu">
  <h3>Crafting</h3>
  <ul>
    {#each Object.entries(items) as [key, value]}
      <li>{key}: {value}</li>
    {/each}
  </ul>
  <div class="actions">
    <label>
      <input type="checkbox" bind:checked={autoCraft} on:change={toggleAuto} />
      Auto-craft
    </label>
    <button on:click={craft}>Craft</button>
    <button on:click={close}>Done</button>
  </div>
</MenuPanel>

<style>
  ul {
    list-style: none;
    padding: 0;
    margin: 0 0 0.5rem 0;
  }
  li {
    font-size: 0.85rem;
  }
  .actions {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }
  button {
    border: 2px solid #fff;
    background: #0a0a0a;
    color: #fff;
    padding: 0.3rem 0.6rem;
  }
</style>

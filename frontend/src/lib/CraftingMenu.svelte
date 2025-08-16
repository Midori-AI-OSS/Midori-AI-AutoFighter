<script>
  import { createEventDispatcher, onMount } from 'svelte';

  import { getGacha, setAutoCraft, craftItems } from './api.js';
  import MenuPanel from './MenuPanel.svelte';

  const iconModules = import.meta.glob('./assets/items/*/*.png', {
    eager: true,
    import: 'default',
    query: '?url'
  });
  const fallbackIcon = new URL('./assets/cards/fallback/placeholder.png', import.meta.url).href;

  const starColors = {
    1: '#808080',
    2: '#228B22',
    3: '#1E90FF',
    4: '#800080',
    5: '#FFD700',
    fallback: '#708090'
  };

  function getIcon(key) {
    const [element, rank] = key.split('_');
    return (
      iconModules[`./assets/items/${element}/generic${rank}.png`] ||
      iconModules[`./assets/items/generic/generic${rank}.png`] ||
      fallbackIcon
    );
  }

  function getStarColor(key) {
    const rank = parseInt(key.split('_')[1]);
    return starColors[rank] || starColors.fallback;
  }

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
  <ul class="item-list">
    {#each Object.entries(items) as [key, value]}
      <li class="item" style={`--star-color: ${getStarColor(key)}`}>
        <img class="item-icon" src={getIcon(key)} alt={key} />
        <span class="label">{key}</span>
        <span class="count">{value}</span>
      </li>
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
  .item {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    font-size: 0.85rem;
  }
  .item-icon {
    width: 24px;
    height: 24px;
    border: 2px solid var(--star-color, #708090);
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

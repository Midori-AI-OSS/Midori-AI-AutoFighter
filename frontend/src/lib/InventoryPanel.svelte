<script>
  import { getRewardArt } from './rewardLoader.js';
  export let cards = [];
  export let relics = [];
  const count = (arr) => {
    const map = {};
    for (const id of arr) {
      map[id] = (map[id] || 0) + 1;
    }
    return Object.entries(map);
  };
</script>

<div class="inv-root" data-testid="inventory-panel">
  {#if cards.length}
    <h3>Cards</h3>
    <div class="grid">
      {#each count(cards) as [id, qty]}
        <div class="item">
          {#if getRewardArt('card', id)}
            <img src={getRewardArt('card', id)} alt={id} />
          {/if}
          <span>{id} x{qty}</span>
        </div>
      {/each}
    </div>
  {/if}
  {#if relics.length}
    <h3>Relics</h3>
    <div class="grid">
      {#each count(relics) as [id, qty]}
        <div class="item">
          {#if getRewardArt('relic', id)}
            <img src={getRewardArt('relic', id)} alt={id} />
          {/if}
          <span>{id} x{qty}</span>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .inv-root { display:flex; flex-direction:column; gap:0.5rem; }
  .grid { display:flex; flex-wrap:wrap; gap:0.5rem; }
  .item { display:flex; flex-direction:column; align-items:center; font-size:0.75rem; }
  .item img { width:48px; height:64px; object-fit:contain; margin-bottom:0.25rem; }
</style>

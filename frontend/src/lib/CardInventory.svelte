<script>
  import MenuPanel from './MenuPanel.svelte';
  export let cards = [];
</script>

<MenuPanel>
  <h3>Card Inventory</h3>
  {#if cards.length === 0}
    <p>No cards collected yet.</p>
  {:else}
    <ul class="cards">
      {#each cards as card}
        <li class="card">{card.name}</li>
      {/each}
    </ul>
  {/if}
</MenuPanel>

<style>
  .cards {
    list-style: none;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  .card {
    border: 2px solid #fff;
    padding: 0.5rem;
    background: #111;
    color: #fff;
  }
</style>

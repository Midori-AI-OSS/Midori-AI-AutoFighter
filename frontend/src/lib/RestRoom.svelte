<script>
  import MenuPanel from './MenuPanel.svelte';
  import CraftingMenu from './CraftingMenu.svelte';
  import { Coins } from 'lucide-svelte';
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  export let gold = 0;
  export let reducedMotion = false;
  let crafting = false;
  function pull() { dispatch('pull'); }
  function swap() { dispatch('swap'); }
  function craft() { crafting = true; }
  function close() { dispatch('close'); }
  function doneCrafting() { crafting = false; }
</script>

{#if crafting}
  <CraftingMenu on:close={doneCrafting} />
{:else}
  <MenuPanel data-testid="rest-room">
    <h3>Rest Room</h3>
    <p class="currency"><Coins size={16} class="coin-icon" class:shine={!reducedMotion} /> {gold}</p>
    <div class="actions">
      <button on:click={pull}>Pull Character</button>
      <button on:click={swap}>Switch Party</button>
      <button on:click={craft}>Craft</button>
      <button on:click={close}>Leave</button>
    </div>
  </MenuPanel>
{/if}

<style>
  .actions {
    display: flex;
    gap: 0.5rem;
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

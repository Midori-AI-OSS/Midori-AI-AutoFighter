<script>
  import MenuPanel from './MenuPanel.svelte';
  import CraftingMenu from './CraftingMenu.svelte';
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
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
</style>

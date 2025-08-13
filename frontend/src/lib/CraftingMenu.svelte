<script>
  import MenuPanel from './MenuPanel.svelte';
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  function close() { dispatch('close'); }
</script>

<MenuPanel data-testid="crafting-menu">
  <h3>Crafting</h3>
  <p>Craft items from gathered materials.</p>
  <button on:click={close}>Done</button>
</MenuPanel>

<style>
  p {
    margin-bottom: 0.5rem;
  }
  button {
    border: 2px solid #fff;
    background: #0a0a0a;
    color: #fff;
    padding: 0.3rem 0.6rem;
  }
</style>

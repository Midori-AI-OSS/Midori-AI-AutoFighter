<script>
  import { createEventDispatcher } from 'svelte';
  export let visible = false;
  const dispatch = createEventDispatcher();
</script>

{#if visible}
  <div class="run-buttons">
    <button class="icon-btn" on:click={() => dispatch('next')}>Next Room</button>
    <button class="icon-btn" on:click={() => dispatch('end')}>End Run</button>
  </div>
{/if}

<style>
  .run-buttons {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
    justify-content: center;
  }
</style>

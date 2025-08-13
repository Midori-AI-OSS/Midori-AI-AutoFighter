<script>
  import { createEventDispatcher } from 'svelte';
  import { Swords, Bed, ShoppingBag, Crown, HelpCircle } from 'lucide-svelte';
  import MenuPanel from './MenuPanel.svelte';

  export let map = [];
  const dispatch = createEventDispatcher();

  function iconFor(room) {
    const r = (room || '').toLowerCase();
    if (r.includes('boss')) return Crown;
    if (r.includes('battle')) return Swords;
    if (r.includes('shop')) return ShoppingBag;
    if (r.includes('rest')) return Bed;
    return HelpCircle;
  }

  function labelFor(room) {
    return (room || '').replace(/-/g, ' ');
  }

  function select(room) {
    dispatch('select', room);
  }
</script>

<MenuPanel>
  <div class="wrap" data-testid="map-display">
    <h4>Map</h4>
    <div class="help">Tap a room to proceed</div>
    <ul>
      {#each map as room}
        <li>
          <button on:click={() => select(room)} data-testid={`room-${room}`}>
            <svelte:component this={iconFor(room)} class="icon" aria-hidden="true" />
            <span class="room-label">{labelFor(room)}</span>
          </button>
        </li>
      {/each}
    </ul>
  </div>
</MenuPanel>

<style>
  .wrap {
    width: min(100%, 640px);
  }
  ul {
    list-style: none;
    padding: 0;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  button {
    border: 2px solid #777;
    background: rgba(0, 0, 0, 0.65);
    color: #fff;
    padding: 0.4rem 0.6rem;
    min-width: 90px;
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  .icon {
    width: 20px;
    height: 20px;
  }
  h4 {
    margin: 0 0 0.5rem 0;
  }
  .help {
    color: #ccc;
    font-size: 0.8rem;
  }
</style>

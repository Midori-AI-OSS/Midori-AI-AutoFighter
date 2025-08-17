<script>
  import { createEventDispatcher } from 'svelte';
  import { Swords, Bed, ShoppingBag, Crown, HelpCircle } from 'lucide-svelte';
  import MenuPanel from './MenuPanel.svelte';
  import { getCharacterImage, getElementColor } from './assetLoader.js';

  export let map = [];
  export let party = [];
  const dispatch = createEventDispatcher();
  let visible = [];
  let current = '';

  $: visible = map.slice(-4);
  $: current = visible[visible.length - 1];

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
    if (room !== current) return;
    dispatch('select', room);
  }
</script>

<MenuPanel>
  {#if party.length}
    <div class="party-preview">
      {#each party as member}
        <img src={getCharacterImage(member.id)} alt="" class="party-icon" style={`border-color: ${getElementColor(member.element)}`} />
      {/each}
    </div>
  {/if}
  <div class="wrap" data-testid="map-display">
    <h4>Map</h4>
    <div class="help">Tap a room to proceed</div>
    <ul>
      {#each visible as room}
        <li>
          <button
            on:click={() => select(room)}
            class:current={room === current}
            disabled={room !== current}
            data-testid={`room-${room}`}
          >
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
  .party-preview {
    display: flex;
    gap: 0.25rem;
    margin-bottom: 0.5rem;
  }
  .party-icon {
    width: 24px;
    height: 24px;
    border: 1px solid #444;
    border-radius: 4px;
  }
  ul {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
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
    opacity: 0.5;
  }
  button.current {
    opacity: 1;
    border-color: #fff;
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

<script>
  import { ArrowLeft } from 'lucide-svelte';
  import RoomView from './RoomView.svelte';
  import PartyPicker from './PartyPicker.svelte';
  import SettingsMenu from './SettingsMenu.svelte';
  import OverlaySurface from './OverlaySurface.svelte';
  import { Diamond, User, Settings, ChevronsRight, Pause } from 'lucide-svelte';
  import { onMount } from 'svelte';
  import { getHourlyBackground } from './assetLoader.js';

  export let runId = '';
  export let roomData = null;
  export let background = '';
  export let viewMode = 'main'; // 'main', 'party', 'settings'
  let randomBg = '';
  let speed2x = false;

  onMount(() => {
    if (!background) {
      randomBg = getHourlyBackground();
    }
  });
  export let selected = [];
</script>

<style>
  .top-right-controls {
    position: absolute;
    top: 1.2rem;
    right: 1.2rem;
    display: flex;
    gap: 0.5rem;
    z-index: 10;
  }
  .viewport-wrap {
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
  .viewport {
    --ui-top-offset: calc(1.2rem + 2.9rem + 1.2rem);
    width: 100%;
    height: 100%;
    border: 2px solid #fff;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    background-image: var(--bg);
    background-size: cover;
    background-position: center;
    overflow: hidden;
  }
  .placeholder {
    color: #ddd;
    font-size: 0.95rem;
    text-align: center;
    backdrop-filter: blur(2px);
    background: rgba(0,0,0,0.35);
    padding: 0.5rem 0.75rem;
  border-radius: 0;
  }
  .overlay-inset {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.85);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
  }
  @media (max-width: 599px) {
    .viewport { aspect-ratio: auto; min-height: 240px; }
  }

  .stained-glass-bar {
    position: absolute;
    top: 1.2rem;
    left: 1.2rem;
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem 0.7rem;
  border-radius: 0;
    background:
      linear-gradient(135deg, rgba(10,10,10,0.96) 0%, rgba(30,30,30,0.92) 100%),
      repeating-linear-gradient(120deg, rgba(255,255,255,0.04) 0 2px, transparent 2px 8px),
      linear-gradient(60deg, rgba(255,255,255,0.06) 10%, rgba(0,0,0,0.38) 80%);
    box-shadow: 0 2px 18px 0 rgba(0,0,0,0.32), 0 1.5px 0 0 rgba(255,255,255,0.04) inset;
    border: 1.5px solid rgba(40,40,40,0.44);
    z-index: 10;
    backdrop-filter: blur(3.5px) saturate(1.05);
    opacity: 0.99;
  }
  .icon-btn {
  background: rgba(255,255,255,0.10);
  border: none;
  border-radius: 0; /* square buttons for game UI */
  width: 2.9rem;
  height: 2.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.18s, box-shadow 0.18s;
  box-shadow: 0 1px 4px 0 rgba(0,40,120,0.10);
  }
  .icon-btn:hover {
    background: rgba(120,180,255,0.22);
    box-shadow: 0 2px 8px 0 rgba(0,40,120,0.18);
  }

</style>

<div class="viewport-wrap">
  <div class="viewport" style={`--bg: url(${background || randomBg})`}>
      <div class="stained-glass-bar">
        <button class="icon-btn" title="Home">
          <Diamond size={22} color="#fff" />
        </button>
        <button class="icon-btn" title="User">
          <User size={22} color="#fff" />
        </button>
        <button class="icon-btn" title="Settings" on:click={() => viewMode = 'settings'}>
          <Settings size={22} color="#fff" />
        </button>
        {#if viewMode !== 'main'}
          <button class="icon-btn" title="Back to Menu" on:click={() => viewMode = 'main'}>
            <ArrowLeft size={22} color="#fff" />
          </button>
        {/if}
      </div>
        <div class="top-right-controls">
          <button class="icon-btn" title="Toggle Speed" on:click={() => (speed2x = !speed2x)}>
            <ChevronsRight size={22} color="#fff" />
          </button>
          <button class="icon-btn" title="Pause" on:click={() => (viewMode = 'settings')}>
            <Pause size={22} color="#fff" />
          </button>
        </div>
        {#if viewMode === 'main'}
          {#if runId && roomData}
            <RoomView result={roomData.result} foes={roomData.foes} party={roomData.party} />
          {:else if runId}
            <div class="placeholder">Select a room on the map to begin</div>
          {/if}
        {/if}
        {#if viewMode === 'party'}
          <OverlaySurface>
            <!-- full party picker overlay: show roster, preview, and stats -->
            <PartyPicker bind:selected={selected} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'settings'}
          <OverlaySurface>
            <SettingsMenu on:close={() => viewMode = 'main'} />
          </OverlaySurface>
        {/if}
  </div>
  
</div>


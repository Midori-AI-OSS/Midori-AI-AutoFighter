<script>
  import { ArrowLeft } from 'lucide-svelte';
  import RoomView from './RoomView.svelte';
  import PartyPicker from './PartyPicker.svelte';
  import SettingsMenu from './SettingsMenu.svelte';
  import OverlaySurface from './OverlaySurface.svelte';
  import MapDisplay from './MapDisplay.svelte';
  import PullsMenu from './PullsMenu.svelte';
  import CraftingMenu from './CraftingMenu.svelte';
  import PlayerEditor from './PlayerEditor.svelte';
  import StatsPanel from './StatsPanel.svelte';
  import { createEventDispatcher } from 'svelte';
  import { Diamond, User, Settings, ChevronsRight, Pause } from 'lucide-svelte';
  import { onMount } from 'svelte';
  import { getHourlyBackground } from './assetLoader.js';

  export let runId = '';
  export let roomData = null;
  export let background = '';
  export let viewMode = 'main'; // 'main', 'party', 'settings'
  export let editorState = {};
  export let map = [];
  export let sfxVolume = 50;
  export let musicVolume = 50;
  export let pauseOnStats = false;
  export let framerate = 60;
  export let autocraft = false;
  let randomBg = '';
  let speed2x = false;
  const dispatch = createEventDispatcher();

  onMount(() => {
    if (!background) {
      randomBg = getHourlyBackground();
    }
  });
  export let selected = [];
  export let items = [];
</script>

<style>
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

  /* right stained-glass sidebar (vertical) */
  .stained-glass-side {
    position: absolute;
    top: calc(var(--ui-top-offset) + 1.2rem);
    right: 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    padding: 0.6rem 0.5rem;
    border-radius: 0;
    background:
      linear-gradient(135deg, rgba(10,10,10,0.96) 0%, rgba(30,30,30,0.92) 100%),
      repeating-linear-gradient(120deg, rgba(255,255,255,0.04) 0 2px, transparent 2px 8px),
      linear-gradient(60deg, rgba(255,255,255,0.03) 10%, rgba(0,0,0,0.45) 80%);
    box-shadow: 0 2px 18px 0 rgba(0,0,0,0.32), 0 1.5px 0 0 rgba(255,255,255,0.02) inset;
    border: 1.5px solid rgba(40,40,40,0.44);
    z-index: 10;
    backdrop-filter: blur(3.5px) saturate(1.05);
    max-height: calc(100% - var(--ui-top-offset) - 2.4rem);
    overflow: auto;
    align-items: center;
  }

  .stained-glass-side .icon-btn {
    width: 3.2rem;
    height: 3.2rem;
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
        <!-- right stained-glass sidebar (mirrors top-left bar styling) -->
        {#if viewMode === 'main'}
          <div class="stained-glass-side">
            {#each items as item}
              <button class="icon-btn" title={item.label} on:click={item.action}>
                {#if item.icon}
                  <svelte:component this={item.icon} size={20} color="#fff" />
                {:else}
                  <span>{item.label}</span>
                {/if}
              </button>
            {/each}
          </div>
        {/if}
        {#if runId && roomData}
          <RoomView result={roomData.result} foes={roomData.foes} party={roomData.party} />
        {:else if runId}
          <div class="placeholder">Select a room on the map to begin</div>
        {/if}
        {#if viewMode === 'party'}
          <OverlaySurface>
            <!-- full party picker overlay: show roster, preview, and stats -->
            <PartyPicker bind:selected={selected} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'map'}
          <OverlaySurface>
            <MapDisplay map={map} on:select={(e) => { /* parent +page listens to MapDisplay via events if needed */ viewMode = 'main'; }} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'party-start'}
          <OverlaySurface>
            <PartyPicker bind:selected={selected} />
            <div style="display:flex;gap:0.5rem;justify-content:flex-end;margin-top:0.5rem;">
              <button class="icon-btn" on:click={() => dispatch('startRun')}>Start Run</button>
              <button class="icon-btn" on:click={() => (viewMode = 'main')}>Cancel</button>
            </div>
          </OverlaySurface>
        {/if}
        {#if viewMode === 'pulls'}
          <OverlaySurface>
            <PullsMenu on:close={() => (viewMode = 'main')} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'craft'}
          <OverlaySurface>
            <CraftingMenu on:close={() => (viewMode = 'main')} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'editor'}
          <OverlaySurface>
            <PlayerEditor {...editorState}
              on:close={() => (viewMode = 'main')}
              on:save={(e) => { dispatch('editorSave', e.detail); viewMode = 'main'; }} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'stats'}
          <OverlaySurface>
            <StatsPanel on:close={() => (viewMode = 'main')} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'settings'}
          <OverlaySurface>
            <SettingsMenu
              {sfxVolume}
              {musicVolume}
              {pauseOnStats}
              {framerate}
              {autocraft}
              on:save={(e) => {
                ({ sfxVolume, musicVolume, pauseOnStats, framerate, autocraft } = e.detail);
                viewMode = 'main';
              }}
              on:close={() => (viewMode = 'main')}
            />
          </OverlaySurface>
        {/if}
  </div>
  
</div>


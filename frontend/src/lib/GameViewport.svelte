<script>
  import { ArrowLeft } from 'lucide-svelte';
  import RoomView from './RoomView.svelte';
  import PartyPicker from './PartyPicker.svelte';
  import SettingsMenu from './SettingsMenu.svelte';
  import OverlaySurface from './OverlaySurface.svelte';
  import MapDisplay from './MapDisplay.svelte';
  import PullsMenu from './PullsMenu.svelte';
  import CraftingMenu from './CraftingMenu.svelte';
  import RewardOverlay from './RewardOverlay.svelte';
  import PlayerEditor from './PlayerEditor.svelte';
  import StatsPanel from './StatsPanel.svelte';
  import { createEventDispatcher } from 'svelte';
  import { Diamond, User, Settings, ChevronsRight } from 'lucide-svelte';
  import { onMount } from 'svelte';
  import { getHourlyBackground } from './assetLoader.js';
  import { loadSettings, saveSettings } from './settingsStorage.js';

  export let runId = '';
  export let roomData = null;
  export let background = '';
  export let viewMode = 'main'; // 'main', 'party', 'settings'
  export let editorState = {};
  export let map = [];
  export let sfxVolume = 50;
  export let musicVolume = 50;
  export let voiceVolume = 50;
  export let framerate = 60;
  export let autocraft = false;
  export let battleActive = false;
  let randomBg = '';
  let speed2x = false;
  const dispatch = createEventDispatcher();

  onMount(() => {
    if (!background) {
      randomBg = getHourlyBackground();
    }
    const saved = loadSettings();
    if (saved.sfxVolume !== undefined) sfxVolume = saved.sfxVolume;
    if (saved.musicVolume !== undefined) musicVolume = saved.musicVolume;
    if (saved.voiceVolume !== undefined) voiceVolume = saved.voiceVolume;
    if (saved.framerate !== undefined) framerate = saved.framerate;
    if (saved.autocraft !== undefined) autocraft = saved.autocraft;
  });
  export let selected = [];
  export let items = [];
</script>

<style>
  .viewport-wrap {
    width: 100%;
    height: 100%;
    overflow: hidden;
    box-sizing: border-box;
  }
  .viewport {
    --ui-top-offset: calc(1.2rem + 2.9rem + 1.2rem);
    width: 100%;
    height: 100%;
    border: 2px solid #fff;
    box-sizing: border-box; /* include border in element's size */
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
  .icon-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .stained-glass-row {
    display: flex;
    gap: 0.5rem;
    justify-content: flex-end;
    margin-top: 0.5rem;
    padding: 0.5rem 0.7rem;
    background:
      linear-gradient(135deg, rgba(10,10,10,0.96) 0%, rgba(30,30,30,0.92) 100%),
      repeating-linear-gradient(120deg, rgba(255,255,255,0.04) 0 2px, transparent 2px 8px),
      linear-gradient(60deg, rgba(255,255,255,0.06) 10%, rgba(0,0,0,0.38) 80%);
    box-shadow: 0 2px 18px 0 rgba(0,0,0,0.32), 0 1.5px 0 0 rgba(255,255,255,0.04) inset;
    border: 1.5px solid rgba(40,40,40,0.44);
    backdrop-filter: blur(3.5px) saturate(1.05);
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
        <button
          class="icon-btn"
          title="Home"
          disabled={battleActive}
          on:click={() => dispatch('home')}
        >
          <Diamond size={22} color="#fff" />
        </button>
        <button
          class="icon-btn"
          title="Player Editor"
          disabled={battleActive}
          on:click={() => dispatch('openEditor')}
        >
          <User size={22} color="#fff" />
        </button>
        <button class="icon-btn" title="Settings" on:click={() => dispatch('settings')}>
          <Settings size={22} color="#fff" />
        </button>
        {#if viewMode !== 'main'}
          <button class="icon-btn" title="Back" on:click={() => dispatch('back')}>
            <ArrowLeft size={22} color="#fff" />
          </button>
        {/if}
      </div>
        <!-- right stained-glass sidebar (mirrors top-left bar styling) -->
        {#if viewMode === 'main'}
          <div class="stained-glass-side">
            {#each items as item}
              <button class="icon-btn" title={item.label} on:click={item.action} disabled={item.disabled}>
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
            <MapDisplay
              map={map}
              on:select={(e) => {
                dispatch('roomSelect', e.detail);
                dispatch('back');
              }}
            />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'party-start'}
          <OverlaySurface>
            <PartyPicker bind:selected={selected} />
            <div class="stained-glass-row">
              <button class="icon-btn" on:click={() => dispatch('startRun')}>Start Run</button>
              <button class="icon-btn" on:click={() => dispatch('back')}>Cancel</button>
            </div>
          </OverlaySurface>
        {/if}
        {#if viewMode === 'pulls'}
          <OverlaySurface>
            <PullsMenu on:close={() => dispatch('back')} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'craft'}
          <OverlaySurface>
            <CraftingMenu on:close={() => dispatch('back')} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'editor'}
          <OverlaySurface>
            <PlayerEditor
              {...editorState}
              on:close={() => dispatch('back')}
              on:save={(e) => {
                dispatch('editorSave', e.detail);
                dispatch('back');
              }}
            />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'stats'}
          <OverlaySurface>
            <StatsPanel on:close={() => dispatch('back')} />
          </OverlaySurface>
        {/if}
        {#if viewMode === 'settings'}
          <OverlaySurface>
            <SettingsMenu
              {sfxVolume}
              {musicVolume}
              {voiceVolume}
              {framerate}
              {autocraft}
              {runId}
              on:save={(e) => {
                ({ sfxVolume, musicVolume, voiceVolume, framerate, autocraft } = e.detail);
                saveSettings({ sfxVolume, musicVolume, voiceVolume, framerate, autocraft });
                dispatch('back');
              }}
              on:close={() => dispatch('back')}
            />
          </OverlaySurface>
        {/if}
        {#if roomData && roomData.card_choices && roomData.card_choices.length > 0}
          <OverlaySurface>
            <RewardOverlay
              cards={roomData.card_choices}
              on:select={(e) => dispatch('rewardSelect', e.detail)}
            />
          </OverlaySurface>
        {/if}
        {#if battleActive && viewMode === 'main'}
          <div class="overlay-inset">
            <div class="placeholder">Battle in progress...</div>
          </div>
        {/if}
  </div>
  
</div>


<script>
  import { onMount } from 'svelte';
  import {
    Play,
    Map,
    Users,
    User,
    Settings,
    SquareChartGantt,
    PackageOpen,
    Hammer
  } from 'lucide-svelte';
  import PartyPicker from '$lib/PartyPicker.svelte';
  import PlayerEditor from '$lib/PlayerEditor.svelte';
  import MapDisplay from '$lib/MapDisplay.svelte';
  import GameViewport from '$lib/GameViewport.svelte';
  import PullsMenu from '$lib/PullsMenu.svelte';
  import CraftingMenu from '$lib/CraftingMenu.svelte';
  import { layoutForWidth } from '$lib/layout.js';
  import {
    startRun,
    battleRoom,
    shopRoom,
    restRoom,
    fetchMap,
    getPlayerConfig,
    savePlayerConfig
  } from '$lib/api.js';

  let width = 0;
  let runId = '';
  let currentMap = [];
  let selectedParty = ['sample_player'];
  let roomData = null;
  let viewportBg = '';
  let viewMode = 'main';
  let showPartyPicker = false;
  let showMap = false;
  let showEditor = false;
  let showPulls = false;
  let showCraft = false;
  let editorState = { pronouns: '', damage: 'Light', hp: 0, attack: 0, defense: 0 };

  function openRun() {
    showPartyPicker = true;
  }

  async function openMap() {
    if (!runId) return;
    const data = await fetchMap(runId);
    currentMap = data.rooms.slice(data.current).map((n) => n.room_type);
    showMap = true;
  }

  async function handleStart() {
    const data = await startRun(selectedParty);
    runId = data.run_id;
    currentMap = data.map.rooms.slice(data.map.current).map((n) => n.room_type);
    showPartyPicker = false;
    showMap = true;
  }

  function handleParty() {
    viewMode = 'party';
  }

  async function openEditor() {
    const data = await getPlayerConfig();
    editorState = data;
    showEditor = true;
  }

  function handleEditorSave(e) {
    editorState = e.detail;
    savePlayerConfig(editorState);
  }

  async function handleRoom(room) {
    if (!runId) return;
    if (room === 'battle') {
      roomData = await battleRoom(runId);
    } else if (room === 'shop') {
      roomData = await shopRoom(runId);
    } else if (room === 'rest') {
      roomData = await restRoom(runId);
    }
    const data = await fetchMap(runId);
    currentMap = data.rooms.slice(data.current).map((n) => n.room_type);
  }

  function openPulls() {
    showPulls = true;
  }

  function openCraft() {
    showCraft = true;
  }

  const items = [
    { icon: Play, label: 'Run', action: openRun },
    { icon: Map, label: 'Map', action: openMap },
    { icon: Users, label: 'Party', action: handleParty },
    { icon: User, label: 'Edit', action: openEditor },
    { icon: PackageOpen, label: 'Pulls', action: openPulls },
    { icon: Hammer, label: 'Craft', action: openCraft },
    { icon: Settings, label: 'Settings', action: () => (viewMode = 'settings') },
    { icon: SquareChartGantt, label: 'Stats' }
  ];

  onMount(() => {
    const update = () => (width = window.innerWidth);
    update();
    window.addEventListener('resize', update);
    return () => window.removeEventListener('resize', update);
  });

  $: mode = layoutForWidth(width);
</script>

<style>
  /* constrain page height and hide overflow */
  :global(html, body) {
    margin: 0;
    padding: 0;
    height: 100vh;
    overflow: hidden;
    background: #000;
    color: #fff;
  }
  /* layout as flex column to structure viewport and panels */
  /* Page split: viewport 75vh and panels auto height */
  .layout {
    display: grid;
    /* viewport fills available space, panels auto height */
    grid-template-rows: 1fr auto;
    height: 100vh;
    gap: 1rem;
    padding: 1rem;
  }

  .menu-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.3rem;
    padding: 0.2rem;
  }

  .cell {
    display: auto;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2px solid #fff;
    padding: 0.3rem;
    background: #111;
    color: #fff;
    cursor: pointer;
    font-size: 0.85rem;
  }

  .cell svg {
    width: 28px;
    height: 28px;
    stroke-width: 2;
    margin-bottom: 0.2rem;
  }

  .panel { border: 2px solid #fff; padding: 0.2rem; background: #0a0a0a; }
  /* Bottom panels container: fill row and hide overflow */
  .stack {
    display: flex;
    flex-direction: column;
  gap: 0.4rem;
  /* allow panel row to size to its content */
  height: auto;
    /* ensure panels fill grid track without overflow */
    overflow: hidden;
  }
  @media (min-width: 1024px) {
    .stack {
      flex-direction: row;
      /* allow shrink to content height */
      height: auto;
      overflow: hidden;
    }
    .stack > section {
      flex: 1;
      /* let section size to content and scroll internally */
      height: auto;
      overflow: auto;
    }
  }
  .section h3 { margin: 0 0 0.2rem 0; font-size: 0.8rem; color: #ddd; }

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Fixed GameViewport height */
  .viewport-wrap {
    /* fill grid row height */
    height: 100%;
    overflow: hidden;
    border: 2px solid #fff;
  }
</style>

<div class="layout">
  <!-- Game Viewport -->
  <div class="viewport-wrap">
    <GameViewport
      runId={runId}
      roomData={roomData}
      background={viewportBg}
      bind:selected={selectedParty}
      bind:viewMode={viewMode}
    />
  </div>

  <div class="stack">
    <section class="panel section">
      <h3>Shortcuts</h3>
      <div class="menu-grid">
        {#each items as item}
          <button type="button" class="cell" on:click={item.action}>
            <svelte:component this={item.icon} />
            <span>{item.label}</span>
          </button>
        {/each}
      </div>
    </section>

    <section class="panel section">
      <h3>Party</h3>
  <PartyPicker compact bind:selected={selectedParty} />
    </section>

    <!-- Player Editor and Stats hidden for now to simplify layout -->
  </div>
</div>
{#if showPartyPicker}
  <div class="overlay">
    <div>
      <PartyPicker bind:selected={selectedParty} />
      <button on:click={handleStart}>Start Run</button>
      <button on:click={() => (showPartyPicker = false)}>Cancel</button>
    </div>
  </div>
{/if}

{#if showEditor}
  <div class="overlay">
    <PlayerEditor
      {...editorState}
      on:save={handleEditorSave}
      on:close={() => (showEditor = false)}
    />
  </div>
{/if}

{#if showMap}
  <div class="overlay">
    <MapDisplay map={currentMap} on:select={(e) => { handleRoom(e.detail); showMap = false; }} />
  </div>
{/if}

{#if showPulls}
  <div class="overlay">
    <PullsMenu on:close={() => (showPulls = false)} />
  </div>
{/if}

{#if showCraft}
  <div class="overlay">
    <CraftingMenu on:close={() => (showCraft = false)} />
  </div>
{/if}

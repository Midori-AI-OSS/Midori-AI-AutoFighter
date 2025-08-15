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
  import StatsPanel from '$lib/StatsPanel.svelte';
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
  let showMap = false;
  let showTarget = false;
  let editorState = { pronouns: '', damage: 'Light', hp: 0, attack: 0, defense: 0 };

  function openRun() {
  viewMode = 'party-start';
  }

  async function openMap() {
  if (!runId) return;
  // show overlay immediately for feedback
  viewMode = 'map';
  const data = await fetchMap(runId);
  currentMap = data.rooms.slice(data.current).map((n) => n.room_type);
  showMap = false; // GameViewport will render map from viewMode 'map'
  }

  async function handleStart() {
    const data = await startRun(selectedParty);
    runId = data.run_id;
    currentMap = data.map.rooms.slice(data.map.current).map((n) => n.room_type);
  viewMode = 'main';
  showMap = true;
  }

  function handleParty() {
    viewMode = 'party';
  }

  async function openEditor() {
    const data = await getPlayerConfig();
    editorState = data;
  viewMode = 'editor';
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
  viewMode = 'pulls';
  }

  function openCraft() {
  viewMode = 'craft';
  }

  function handleTarget() {
    showTarget = true;
  }

  async function pollServer() {
    if (!runId) return;
    const data = await fetchMap(runId);
    currentMap = data.rooms.slice(data.current).map((n) => n.room_type);
  }

  const items = [
    { icon: Play, label: 'Run', action: openRun },
    { icon: Map, label: 'Map', action: openMap },
    { icon: Users, label: 'Party', action: handleParty },
    { icon: User, label: 'Edit', action: openEditor },
    { icon: PackageOpen, label: 'Pulls', action: openPulls },
    { icon: Hammer, label: 'Craft', action: openCraft },
    { icon: Settings, label: 'Settings', action: () => (viewMode = 'settings') },
  { icon: SquareChartGantt, label: 'Stats', action: () => (viewMode = 'stats') }
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
    grid-template-rows: 75vh auto;
    height: 100vh;
    gap: 1rem;
    padding: 1rem;
  }

  @media (min-width: 1024px) {
    .layout {
      grid-template-columns: 20rem 1fr;
      grid-template-rows: 1fr;
    }
  }

  .panel { border: 2px solid #fff; padding: 0.2rem; background: #0a0a0a; }
  .section h3 { margin: 0 0 0.2rem 0; font-size: 0.8rem; color: #ddd; }
  .side { position: relative; }
  .target-panel {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    transform: translateY(-100%);
    transition: transform 0.25s ease;
  }
  .target-panel.show {
    transform: translateY(0);
  }

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
  <div class="side">
    <section class="panel section">
      <h3>Party</h3>
      <PartyPicker compact bind:selected={selectedParty} on:click={handleTarget} />
      <div class="target-panel" class:show={showTarget}>
        <StatsPanel on:close={() => (showTarget = false)} />
      </div>
    </section>
  </div>

  <div class="viewport-wrap">
    <GameViewport
      runId={runId}
      roomData={roomData}
      background={viewportBg}
      bind:selected={selectedParty}
      bind:viewMode={viewMode}
      items={items}
      editorState={editorState}
      map={currentMap}
      on:startRun={() => { handleStart(); viewMode = 'main'; }}
      on:editorSave={(e) => { handleEditorSave(e); viewMode = 'main'; }}
      on:target={handleTarget}
      on:poll={pollServer}
    />
  </div>
</div>

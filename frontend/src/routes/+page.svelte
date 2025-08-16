<script>
  import {
    Play,
    Map,
    Users,
    User,
    Settings,
    SquareChartGantt,
    PackageOpen,
    Hammer,
    MessageSquare
  } from 'lucide-svelte';
  import GameViewport from '$lib/GameViewport.svelte';
  import {
    startRun,
    fetchMap,
    getPlayerConfig,
    savePlayerConfig,
    roomAction,
    chooseCard
  } from '$lib/api.js';
  import { FEEDBACK_URL } from '$lib/constants.js';

  let runId = '';
  let currentMap = [];
  let selectedParty = ['sample_player'];
  let roomData = null;
  let viewportBg = '';
  let viewMode = 'main';
  let viewStack = [];

  function setView(mode) {
    viewStack.push(viewMode);
    viewMode = mode;
  }

  function goBack() {
    viewMode = viewStack.pop() || 'main';
  }

  function goHome() {
    viewStack = [];
    viewMode = 'main';
  }
  let editorState = { pronouns: '', damageType: 'Light', hp: 0, attack: 0, defense: 0 };
  let battleActive = false;

  function openRun() {
    setView('party-start');
  }

  async function checkBattle() {
    if (!runId) return false;
    const data = await fetchMap(runId);
    const map = data.map;
    currentMap = map.rooms.slice(map.current).map((n) => n.room_type);
    battleActive = map.battle;
    return battleActive;
  }

  async function openMap() {
    if (!runId) return;
    if (await checkBattle()) return;
    setView('map');
  }

  async function handleStart() {
    const data = await startRun(selectedParty);
    runId = data.run_id;
    currentMap = data.map.rooms.slice(data.map.current).map((n) => n.room_type);
    battleActive = data.map.battle;
    viewStack = ['main'];
    viewMode = 'map';
  }

  async function handleParty() {
    if (await checkBattle()) return;
    setView('party');
  }

  async function openEditor() {
    if (await checkBattle()) return;
    const data = await getPlayerConfig();
    editorState = {
      pronouns: data.pronouns,
      damageType: data.damage_type,
      hp: data.hp,
      attack: data.attack,
      defense: data.defense,
    };
    setView('editor');
  }

  function handleEditorSave(e) {
    editorState = {
      ...e.detail,
      hp: +e.detail.hp,
      attack: +e.detail.attack,
      defense: +e.detail.defense,
    };
    savePlayerConfig({
      pronouns: editorState.pronouns,
      damage_type: editorState.damageType,
      hp: editorState.hp,
      attack: editorState.attack,
      defense: editorState.defense,
    });
  }

  async function openPulls() {
    if (await checkBattle()) return;
    setView('pulls');
  }

  async function openCraft() {
    if (await checkBattle()) return;
    setView('craft');
  }

  function openFeedback() {
    window.open(FEEDBACK_URL, '_blank', 'noopener');
  }

  async function handleTarget() {
    if (await checkBattle()) return;
    setView('stats');
  }

  async function handleRoomSelect(e) {
    if (!runId || battleActive) return;
    const room = e.detail;
    let data;
    if (room.includes('battle')) {
      battleActive = true;
      data = await roomAction(runId, 'battle');
    } else if (room.includes('shop')) {
      data = await roomAction(runId, 'shop');
    } else if (room.includes('rest')) {
      data = await roomAction(runId, 'rest');
    } else if (room.includes('boss')) {
      battleActive = true;
      data = await roomAction(runId, 'boss');
    } else {
      return;
    }
    roomData = data;
    await checkBattle();
  }

  async function handleRewardSelect(detail) {
    if (!runId) return;
    await chooseCard(runId, detail.id);
    if (roomData) {
      roomData.card_choices = [];
    }
  }
  let items = [];
  $: items = [
    { icon: Play, label: 'Run', action: openRun, disabled: battleActive },
    { icon: Map, label: 'Map', action: openMap, disabled: battleActive },
    { icon: Users, label: 'Party', action: handleParty, disabled: battleActive },
    { icon: User, label: 'Edit', action: openEditor, disabled: battleActive },
    { icon: PackageOpen, label: 'Pulls', action: openPulls, disabled: battleActive },
    { icon: Hammer, label: 'Craft', action: openCraft, disabled: battleActive },
    {
      icon: Settings,
      label: 'Settings',
      action: () => setView('settings'),
      disabled: false
    },
    { icon: MessageSquare, label: 'Feedback', action: openFeedback, disabled: false },
    { icon: SquareChartGantt, label: 'Stats', action: handleTarget, disabled: battleActive }
  ];

</script>

<style>
  :global(html, body) {
    margin: 0;
    padding: 0;
    height: 100vh;
    /* allow scrolling when content is larger than the viewport
       (prevent content from being clipped at the right/bottom) */
    overflow: auto;
    background: #000;
    color: #fff;
    box-sizing: border-box;
  }

  /* Make the viewport container responsive and avoid forcing a second
     full-height which can overflow when inner elements have borders/padding. */
  .viewport-wrap {
    width: 100%;
    max-width: 98vw;
    max-height: 98vh;
    height: 100%;
    margin: 0 auto;
    box-sizing: border-box;
    /* allow inner UI panels to scroll if they grow beyond available space */
    overflow: auto;
    padding: 0 0.5rem; /* small horizontal padding so elements don't touch the edge */
  }
</style>

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
    battleActive={battleActive}
    on:startRun={handleStart}
    on:editorSave={(e) => handleEditorSave(e)}
    on:target={handleTarget}
    on:roomSelect={handleRoomSelect}
    on:back={goBack}
    on:home={goHome}
    on:openEditor={openEditor}
    on:settings={() => setView('settings')}
    on:rewardSelect={(e) => handleRewardSelect(e.detail)}
  />
</div>

<script>
  import GameViewport from '$lib/GameViewport.svelte';
  import { onMount } from 'svelte';
  import {
    startRun,
    roomAction,
    chooseCard,
    chooseRelic,
    advanceRoom,
    getMap,
    updateParty
  } from '$lib/runApi.js';
  import { getPlayerConfig, savePlayerConfig } from '$lib/api.js';
  import { loadRunState, saveRunState, clearRunState } from '$lib/runState.js';
  import { FEEDBACK_URL } from '$lib/constants.js';
  import MainMenu from '$lib/MainMenu.svelte';
  import RunButtons from '$lib/RunButtons.svelte';

  let runId = '';
  let selectedParty = ['sample_player'];
  let roomData = null;
  // Track map state to render room/floor context in battle header
  let mapRooms = [];
  let currentIndex = 0;
  let currentRoomType = '';
  let viewportBg = '';
  let viewMode = 'main';
  let viewStack = [];
  let nextRoom = '';

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

  onMount(async () => {
    const saved = loadRunState();
    if (saved) {
      try {
        const { runId: storedId } = saved;
        const data = await getMap(storedId);
        runId = storedId;
        selectedParty = data.party || selectedParty;
        mapRooms = data.map.rooms || [];
        currentIndex = data.map.current || 0;
        nextRoom = mapRooms[currentIndex]?.room_type || '';
        currentRoomType = nextRoom || '';
        await enterRoom();
      } catch {
        clearRunState();
      }
    }
  });

  function openRun() {
    if (runId) {
      viewMode = 'main';
      if (!battleActive && nextRoom) {
        enterRoom();
      }
    } else {
      setView('party-start');
    }
  }

  function handleRunEnd() {
    stopBattlePoll();
    runId = '';
    roomData = null;
    nextRoom = '';
    battleActive = false;
    viewStack = [];
    viewMode = 'main';
    clearRunState();
  }

  async function handleStart() {
    const data = await startRun(selectedParty);
    runId = data.run_id;
    mapRooms = data.map.rooms || [];
    currentIndex = data.map.current || 0;
    nextRoom = mapRooms[currentIndex]?.room_type || '';
    currentRoomType = nextRoom || '';
    viewStack = ['main'];
    viewMode = 'main';
    await enterRoom();
  }

  async function handleParty() {
    if (battleActive) return;
    setView('party');
  }

  async function handlePartySave() {
    if (runId) {
      await updateParty(runId, selectedParty);
    }
    goBack();
  }

  async function openEditor() {
    if (battleActive) return;
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

  async function handleEditorSave(e) {
    editorState = {
      ...e.detail,
      hp: +e.detail.hp,
      attack: +e.detail.attack,
      defense: +e.detail.defense,
    };
    await savePlayerConfig({
      pronouns: editorState.pronouns,
      damage_type: editorState.damageType,
      hp: editorState.hp,
      attack: editorState.attack,
      defense: editorState.defense,
    });
  }

  async function openPulls() {
    if (battleActive) return;
    setView('pulls');
  }

  async function openCraft() {
    if (battleActive) return;
    setView('craft');
  }

  function openFeedback() {
    window.open(FEEDBACK_URL, '_blank', 'noopener');
  }

  async function openInventory() {
    if (battleActive) return;
    setView('inventory');
  }

  let battleTimer;

  function stopBattlePoll() {
    if (battleTimer) {
      clearTimeout(battleTimer);
      battleTimer = null;
    }
  }

  async function pollBattle() {
    if (!battleActive) return;
    try {
      const snap = await roomAction(runId, 'battle', 'snapshot');
      if (snap?.loot) {
        roomData = snap;
        battleActive = false;
        nextRoom = snap.next_room || nextRoom;
        if (typeof snap.current_index === 'number') currentIndex = snap.current_index;
        if (snap.current_room) currentRoomType = snap.current_room;
        return;
      }
    } catch {
      /* ignore */
    }
    battleTimer = setTimeout(pollBattle, 1000 / 60);
  }

  async function enterRoom() {
    stopBattlePoll();
    if (!runId || !nextRoom) return;
    let endpoint = nextRoom;
    if (endpoint.includes('battle')) {
      endpoint = nextRoom.includes('boss') ? 'boss' : 'battle';
    }
    // Fetch first, then decide whether to show rewards or start battle polling.
    const data = await roomAction(runId, endpoint);
    roomData = data;
    if (data.party) {
      selectedParty = data.party.map((p) => p.id);
    }
    // Keep map-derived indices and current room type in sync when available
    if (typeof data.current_index === 'number') currentIndex = data.current_index;
    if (data.current_room) currentRoomType = data.current_room;
    nextRoom = data.next_room || '';
    saveRunState(runId, nextRoom);
    if (endpoint === 'battle') {
      const hasRewards = Boolean(data?.loot) || (data?.card_choices?.length > 0) || (data?.relic_choices?.length > 0);
      if (hasRewards) {
        battleActive = false;
        return;
      }
      const noFoes = !Array.isArray(data?.foes) || data.foes.length === 0;
      if (noFoes) {
        // Try to fetch the saved battle snapshot (e.g., after refresh while awaiting rewards).
        try {
          const snap = await roomAction(runId, 'battle', 'snapshot');
          const snapHasRewards = Boolean(snap?.loot) || (snap?.card_choices?.length > 0) || (snap?.relic_choices?.length > 0);
          if (snapHasRewards) {
            roomData = snap;
            battleActive = false;
            nextRoom = snap.next_room || nextRoom;
            if (typeof snap.current_index === 'number') currentIndex = snap.current_index;
            if (snap.current_room) currentRoomType = snap.current_room;
            return;
          }
        } catch {}
      }
      // If the snapshot didn't include current room type yet, fall back to pre-room value
      if (!currentRoomType) currentRoomType = endpoint.includes('boss') ? 'battle-boss-floor' : 'battle-normal';
      battleActive = true;
      pollBattle();
    } else {
      battleActive = false;
    }
  }

  async function handleRewardSelect(detail) {
    if (!runId) return;
    let res;
    if (detail.type === 'card') {
      res = await chooseCard(runId, detail.id);
      if (roomData) roomData.card_choices = [];
    } else if (detail.type === 'relic') {
      res = await chooseRelic(runId, detail.id);
      if (roomData) roomData.relic_choices = [];
    }
    if (res && res.next_room) {
      nextRoom = res.next_room;
    }
  }
  async function handleShopBuy(item) {
    if (!runId) return;
    roomData = await roomAction(runId, 'shop', item);
  }
  async function handleShopReroll() {
    if (!runId) return;
    roomData = await roomAction(runId, 'shop', 'reroll');
  }
  async function handleShopLeave() {
    if (!runId) return;
    await roomAction(runId, 'shop', 'leave');
    const res = await advanceRoom(runId);
    if (res && res.next_room) {
      nextRoom = res.next_room;
    }
    await enterRoom();
  }
  async function handleRestPull() {
    if (!runId) return;
    roomData = await roomAction(runId, 'rest', 'pull');
  }
  async function handleRestSwap() {
    if (!runId) return;
    roomData = await roomAction(runId, 'rest', 'swap');
  }
  async function handleRestCraft() {
    if (!runId) return;
    roomData = await roomAction(runId, 'rest', 'craft');
  }
  async function handleRestLeave() {
    if (!runId) return;
    await roomAction(runId, 'rest', 'leave');
    const res = await advanceRoom(runId);
    if (res && res.next_room) {
      nextRoom = res.next_room;
    }
    await enterRoom();
  }

  async function handleNextRoom() {
    if (!runId) return;
    await advanceRoom(runId);
    await enterRoom();
  }
  let items = [];

</script>

<style>
  :global(:root) {
    --glass-bg: linear-gradient(135deg, rgba(10,10,10,0.96) 0%, rgba(30,30,30,0.92) 100%),
      repeating-linear-gradient(120deg, rgba(255,255,255,0.04) 0 2px, transparent 2px 8px),
      linear-gradient(60deg, rgba(255,255,255,0.06) 10%, rgba(0,0,0,0.38) 80%);
    --glass-border: 1.5px solid rgba(40,40,40,0.44);
    --glass-shadow: 0 2px 18px 0 rgba(0,0,0,0.32), 0 1.5px 0 0 rgba(255,255,255,0.04) inset;
    --glass-filter: blur(3.5px) saturate(1.05);
  }
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
    /* avoid horizontal scrollbar; allow vertical scrolling */
    overflow-x: hidden;
    overflow-y: auto;
    padding: 0 0.5rem; /* small horizontal padding so elements don't touch the edge */
  }
</style>

<MainMenu
  bind:items
  run={openRun}
  party={handleParty}
  edit={openEditor}
  pulls={openPulls}
  craft={openCraft}
  settings={() => setView('settings')}
  feedback={openFeedback}
  inventory={openInventory}
  {battleActive}
/>

<div class="viewport-wrap">
  <GameViewport
    runId={runId}
    roomData={roomData}
    background={viewportBg}
    mapRooms={mapRooms}
    currentIndex={currentIndex}
    currentRoomType={currentRoomType}
    bind:selected={selectedParty}
    bind:viewMode={viewMode}
    items={items}
    editorState={editorState}
    battleActive={battleActive}
    on:startRun={handleStart}
    on:editorSave={(e) => handleEditorSave(e)}
    on:target={openInventory}
    on:back={goBack}
    on:home={goHome}
    on:openEditor={openEditor}
    on:settings={() => setView('settings')}
    on:rewardSelect={(e) => handleRewardSelect(e.detail)}
    on:shopBuy={(e) => handleShopBuy(e.detail)}
    on:shopReroll={handleShopReroll}
    on:shopLeave={handleShopLeave}
    on:restPull={handleRestPull}
    on:restSwap={handleRestSwap}
    on:restCraft={handleRestCraft}
    on:restLeave={handleRestLeave}
    on:nextRoom={handleNextRoom}
    on:endRun={handleRunEnd}
    on:saveParty={handlePartySave}
  />
  <RunButtons visible={runId && !battleActive} on:next={handleNextRoom} on:end={handleRunEnd} />
</div>

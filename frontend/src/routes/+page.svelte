<script>
  import {
    Play,
    Users,
    User,
    Settings,
    Package,
    PackageOpen,
    Hammer,
    MessageSquare
  } from 'lucide-svelte';
  import GameViewport from '$lib/GameViewport.svelte';
  import {
    startRun,
    getPlayerConfig,
    savePlayerConfig,
    roomAction,
    chooseCard,
    chooseRelic,
    advanceRoom
  } from '$lib/api.js';
  import { FEEDBACK_URL } from '$lib/constants.js';

  let runId = '';
  let selectedParty = ['sample_player'];
  let roomData = null;
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

  async function handleStart() {
    const data = await startRun(selectedParty);
    runId = data.run_id;
    nextRoom = data.map.rooms[data.map.current].room_type;
    viewStack = ['main'];
    viewMode = 'main';
    await enterRoom();
  }

  async function handleParty() {
    if (battleActive) return;
    setView('party');
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
    if (endpoint === 'battle') {
      battleActive = true;
    }
    const data = await roomAction(runId, endpoint);
    roomData = data;
    nextRoom = data.next_room || '';
    if (endpoint === 'battle') {
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
    await advanceRoom(runId);
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
    await advanceRoom(runId);
    await enterRoom();
  }

  async function handleNextRoom() {
    if (!runId) return;
    await advanceRoom(runId);
    await enterRoom();
  }
  let items = [];
  $: items = [
    { icon: Play, label: 'Run', action: openRun, disabled: false },
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
    { icon: Package, label: 'Inventory', action: openInventory, disabled: battleActive }
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
  />
</div>

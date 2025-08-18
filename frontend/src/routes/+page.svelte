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
    chooseCard
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

  async function enterRoom() {
    if (!runId || !nextRoom) return;
    let endpoint = nextRoom;
    if (endpoint.includes('battle')) {
      endpoint = nextRoom.includes('boss') ? 'boss' : 'battle';
    }
    const data = await roomAction(runId, endpoint);
    roomData = data;
    nextRoom = data.next_room || '';
    battleActive = data.result === 'battle' || data.result === 'boss';
    if (
      !battleActive &&
      (!data.card_choices || data.card_choices.length === 0) &&
      nextRoom &&
      data.result !== 'shop' &&
      data.result !== 'rest'
    ) {
      await enterRoom();
    }
  }

  async function handleRewardSelect(detail) {
    if (!runId) return;
    await chooseCard(runId, detail.id);
    if (roomData) {
      roomData.card_choices = [];
    }
    await enterRoom();
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
  />
</div>

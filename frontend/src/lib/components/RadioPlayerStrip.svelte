<script>
  import { createEventDispatcher } from 'svelte';
  import { Pause, Play, SkipBack, SkipForward, Volume2 } from 'lucide-svelte';

  export let runtime = {
    channels: ['all'],
    channel: 'all',
    activeQuality: 'medium',
    pendingQuality: null,
    volume: 70,
    isPlaying: false,
    playbackDesired: false,
    connectionState: 'idle',
    statusText: 'Idle',
    currentTrack: null,
    artUrl: '',
    lastError: null,
  };

  const dispatch = createEventDispatcher();

  let dragStartX = null;
  let dragDelta = 0;

  function onPointerDown(event) {
    if (event.pointerType === 'mouse' && event.button !== 0) return;
    dragStartX = event.clientX;
    dragDelta = 0;
  }

  function onPointerMove(event) {
    if (dragStartX === null) return;
    dragDelta = event.clientX - dragStartX;
  }

  function onPointerUp() {
    if (dragStartX === null) return;
    const threshold = 56;
    if (dragDelta <= -threshold) {
      dispatch('nextChannel');
    } else if (dragDelta >= threshold) {
      dispatch('previousChannel');
    }
    dragStartX = null;
    dragDelta = 0;
  }

  function onPointerCancel() {
    dragStartX = null;
    dragDelta = 0;
  }

  $: desiredQuality = (runtime.pendingQuality || runtime.activeQuality || 'medium').toLowerCase();
  $: qualityLabel = desiredQuality === 'high' ? 'HQ' : 'MQ';
  $: title = runtime.currentTrack?.title || 'Fetching current track…';
  $: subtitle = (() => {
    const channel = String(runtime.channel || 'all');
    const stateText = runtime.lastError ? 'Error' : (runtime.statusText || 'Idle');
    return `Channel: ${channel} · ${stateText}`;
  })();
  $: backdropStyle = runtime.artUrl ? `background-image: url('${runtime.artUrl}');` : '';
</script>

<div
  class="radio-strip"
  data-state={runtime.connectionState}
  on:pointerdown={onPointerDown}
  on:pointermove={onPointerMove}
  on:pointerup={onPointerUp}
  on:pointercancel={onPointerCancel}
>
  <div class="backdrop" style={backdropStyle}></div>
  <div class="overlay"></div>

  <div class="content">
    <div class="meta">
      <div class="title" title={title}>{title}</div>
      <div class="subtitle" title={subtitle}>{subtitle}</div>
    </div>

    <div class="controls" role="group" aria-label="Radio controls">
      <button class="icon-btn" aria-label="Previous channel" on:click={() => dispatch('previousChannel')}>
        <SkipBack size={18} />
      </button>
      <button class="icon-btn play" aria-label={runtime.isPlaying ? 'Pause playback' : 'Start playback'} on:click={() => dispatch('togglePlayback')}>
        {#if runtime.isPlaying || runtime.playbackDesired}
          <Pause size={20} />
        {:else}
          <Play size={20} />
        {/if}
      </button>
      <button class="icon-btn" aria-label="Next channel" on:click={() => dispatch('nextChannel')}>
        <SkipForward size={18} />
      </button>
    </div>

    <div class="selectors">
      <label>
        <span class="sr-only">Channel</span>
        <select value={runtime.channel} on:change={(event) => dispatch('setChannel', event.currentTarget.value)}>
          {#each (runtime.channels?.length ? runtime.channels : ['all']) as channelName}
            <option value={channelName}>{channelName}</option>
          {/each}
        </select>
      </label>
      <button class="quality-btn" aria-label="Toggle radio quality" on:click={() => dispatch('toggleQuality')}>
        {qualityLabel}
      </button>
      <label class="volume-wrap">
        <Volume2 size={14} />
        <input
          type="range"
          min="0"
          max="100"
          step="1"
          value={runtime.volume}
          aria-label="Radio volume"
          on:input={(event) => dispatch('setVolume', Number(event.currentTarget.value))}
        />
      </label>
    </div>
  </div>
</div>

<style>
  .radio-strip {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    min-height: 78px;
    z-index: 9800;
    overflow: hidden;
    border-top: 1px solid rgba(255, 255, 255, 0.16);
    box-shadow: 0 -8px 36px rgba(0, 0, 0, 0.42);
    touch-action: pan-y;
  }

  .backdrop {
    position: absolute;
    inset: -8px;
    background-size: cover;
    background-position: center;
    filter: blur(12px) saturate(1.05);
    transform: scale(1.05);
    opacity: 0.48;
    pointer-events: none;
  }

  .overlay {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
      linear-gradient(180deg, rgba(7, 11, 20, 0.56), rgba(8, 12, 18, 0.92)),
      linear-gradient(120deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0));
  }

  .content {
    position: relative;
    display: grid;
    grid-template-columns: minmax(220px, 1fr) auto auto;
    gap: 0.65rem;
    align-items: center;
    padding: 0.55rem 0.75rem 0.65rem;
  }

  .meta {
    min-width: 0;
  }

  .title {
    font-size: 0.86rem;
    font-weight: 700;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .subtitle {
    margin-top: 0.18rem;
    opacity: 0.8;
    font-size: 0.74rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .controls {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
  }

  .icon-btn,
  .quality-btn {
    appearance: none;
    border: 1px solid rgba(255, 255, 255, 0.26);
    background: rgba(14, 20, 32, 0.66);
    color: inherit;
    min-height: 34px;
    min-width: 34px;
    border-radius: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 0 0.45rem;
  }

  .icon-btn:focus-visible,
  .quality-btn:focus-visible,
  .selectors select:focus-visible,
  .selectors input[type='range']:focus-visible {
    outline: 2px solid rgba(145, 205, 255, 0.86);
    outline-offset: 2px;
  }

  .icon-btn.play {
    min-width: 38px;
    min-height: 38px;
  }

  .selectors {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }

  .selectors select {
    appearance: none;
    border: 1px solid rgba(255, 255, 255, 0.26);
    background: rgba(14, 20, 32, 0.66);
    color: inherit;
    border-radius: 0;
    min-height: 34px;
    padding: 0 0.5rem;
    max-width: 10rem;
  }

  .quality-btn {
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    min-width: 42px;
  }

  .volume-wrap {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    border: 1px solid rgba(255, 255, 255, 0.26);
    background: rgba(14, 20, 32, 0.66);
    padding: 0 0.35rem;
    min-height: 34px;
  }

  .volume-wrap input[type='range'] {
    width: 92px;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }

  @media (max-width: 900px) {
    .content {
      grid-template-columns: 1fr;
      gap: 0.45rem;
      padding-bottom: calc(0.65rem + env(safe-area-inset-bottom, 0px));
    }

    .controls,
    .selectors {
      justify-content: center;
    }

    .meta {
      text-align: center;
    }
  }
</style>

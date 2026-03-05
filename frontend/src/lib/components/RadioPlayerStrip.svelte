<script>
  import { createEventDispatcher, onDestroy } from 'svelte';
  import { AudioLines, Pause, Play, SkipBack, SkipForward, Volume2 } from 'lucide-svelte';

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

  const SWIPE_THRESHOLD_PX = 56;
  const COLLAPSE_DELAY_MS = 3000;
  const FALLBACK_PALETTE = {
    primary: '30, 43, 66',
    secondary: '79, 122, 219',
    glow: '129, 209, 255',
    dim: '8, 11, 18',
  };

  const paletteCache = new Map();

  let dragStartX = null;
  let dragDelta = 0;
  let hovered = false;
  let expanded = true;
  let collapseTimer = null;
  let paletteToken = 0;
  let activePalette = FALLBACK_PALETTE;
  let lastPaletteUrl = '';

  function clearCollapseTimer() {
    if (collapseTimer !== null) {
      clearTimeout(collapseTimer);
      collapseTimer = null;
    }
  }

  function scheduleCollapse() {
    clearCollapseTimer();
    collapseTimer = setTimeout(() => {
      if (!hovered) {
        expanded = false;
      }
    }, COLLAPSE_DELAY_MS);
  }

  function handlePointerEnter() {
    hovered = true;
    clearCollapseTimer();
    expanded = true;
  }

  function handlePointerLeave() {
    hovered = false;
    scheduleCollapse();
  }

  function canStartSwipe(event) {
    if (!expanded) return false;
    if (!(event.target instanceof Element)) return true;
    return !event.target.closest('button, select, input, label, [data-no-swipe]');
  }

  function onPointerDown(event) {
    if (event.pointerType === 'mouse' && event.button !== 0) return;
    if (!canStartSwipe(event)) return;
    dragStartX = event.clientX;
    dragDelta = 0;
  }

  function onPointerMove(event) {
    if (dragStartX === null) return;
    dragDelta = event.clientX - dragStartX;
  }

  function resetSwipe() {
    dragStartX = null;
    dragDelta = 0;
  }

  function onPointerUp() {
    if (dragStartX === null) return;
    if (dragDelta <= -SWIPE_THRESHOLD_PX) {
      dispatch('nextChannel');
    } else if (dragDelta >= SWIPE_THRESHOLD_PX) {
      dispatch('previousChannel');
    }
    resetSwipe();
  }

  function onPointerCancel() {
    resetSwipe();
  }

  function clampChannelLabel(value) {
    const normalized = String(value || 'all').trim();
    return normalized || 'all';
  }

  function mixColor(a, b, ratio) {
    return {
      r: Math.round((a.r * (1 - ratio)) + (b.r * ratio)),
      g: Math.round((a.g * (1 - ratio)) + (b.g * ratio)),
      b: Math.round((a.b * (1 - ratio)) + (b.b * ratio)),
    };
  }

  function toCsv(color) {
    return `${color.r}, ${color.g}, ${color.b}`;
  }

  function saturationScore(r, g, b) {
    const high = Math.max(r, g, b);
    const low = Math.min(r, g, b);
    if (high <= 0) return 0;
    return (high - low) / high;
  }

  async function extractPalette(url) {
    if (!url || typeof window === 'undefined') {
      return FALLBACK_PALETTE;
    }

    const image = await new Promise((resolve, reject) => {
      const node = new Image();
      node.crossOrigin = 'anonymous';
      node.referrerPolicy = 'no-referrer';
      node.onload = () => resolve(node);
      node.onerror = reject;
      node.src = url;
    });

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d', { willReadFrequently: true });
    if (!context) {
      return FALLBACK_PALETTE;
    }

    canvas.width = 48;
    canvas.height = 48;
    context.drawImage(image, 0, 0, canvas.width, canvas.height);

    const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;

    let totalR = 0;
    let totalG = 0;
    let totalB = 0;
    let count = 0;
    let mostVibrant = { r: 79, g: 122, b: 219 };
    let mostVibrantScore = -1;

    for (let index = 0; index < pixels.length; index += 16) {
      const r = pixels[index];
      const g = pixels[index + 1];
      const b = pixels[index + 2];
      const a = pixels[index + 3];
      if (a < 100) continue;

      totalR += r;
      totalG += g;
      totalB += b;
      count += 1;

      const sat = saturationScore(r, g, b);
      const luminance = (r + g + b) / 765;
      const score = sat * Math.max(0.2, luminance);
      if (score > mostVibrantScore) {
        mostVibrantScore = score;
        mostVibrant = { r, g, b };
      }
    }

    if (count === 0) {
      return FALLBACK_PALETTE;
    }

    const average = {
      r: Math.round(totalR / count),
      g: Math.round(totalG / count),
      b: Math.round(totalB / count),
    };

    const primary = mixColor(average, { r: 10, g: 13, b: 20 }, 0.45);
    const secondary = mixColor(mostVibrant, average, 0.15);
    const glow = mixColor(mostVibrant, { r: 190, g: 235, b: 255 }, 0.35);
    const dim = mixColor(primary, { r: 6, g: 8, b: 12 }, 0.65);

    return {
      primary: toCsv(primary),
      secondary: toCsv(secondary),
      glow: toCsv(glow),
      dim: toCsv(dim),
    };
  }

  async function updatePalette(url) {
    const token = ++paletteToken;
    if (!url) {
      activePalette = FALLBACK_PALETTE;
      return;
    }

    if (paletteCache.has(url)) {
      activePalette = paletteCache.get(url);
      return;
    }

    try {
      const palette = await extractPalette(url);
      paletteCache.set(url, palette);
      if (token === paletteToken) {
        activePalette = palette;
      }
    } catch {
      if (token === paletteToken) {
        activePalette = FALLBACK_PALETTE;
      }
    }
  }

  $: desiredQuality = (runtime.pendingQuality || runtime.activeQuality || 'medium').toLowerCase();
  $: isQualityHigh = desiredQuality === 'high';
  $: qualityAriaLabel = isQualityHigh ? 'Switch to medium quality' : 'Switch to high quality';
  $: title = runtime.currentTrack?.title || 'Fetching current track...';
  $: subtitle = `Midori AI Radio: ${clampChannelLabel(runtime.channel)}`;
  $: backdropStyle = runtime.artUrl ? `background-image: url('${runtime.artUrl}');` : '';
  $: paletteStyle = `--radio-primary: ${activePalette.primary}; --radio-secondary: ${activePalette.secondary}; --radio-glow: ${activePalette.glow}; --radio-dim: ${activePalette.dim};`;

  $: {
    const currentUrl = String(runtime.artUrl || '').trim();
    if (currentUrl !== lastPaletteUrl) {
      lastPaletteUrl = currentUrl;
      void updatePalette(currentUrl);
    }
  }

  onDestroy(() => {
    clearCollapseTimer();
  });
</script>

<div
  class="radio-strip"
  class:expanded
  class:collapsed={!expanded}
  data-state={runtime.connectionState}
  style={paletteStyle}
  on:pointerenter={handlePointerEnter}
  on:pointerleave={handlePointerLeave}
  on:pointerdown={onPointerDown}
  on:pointermove={onPointerMove}
  on:pointerup={onPointerUp}
  on:pointercancel={onPointerCancel}
>
  <div class="bg-art" style={backdropStyle}></div>
  <div class="bg-glow"></div>
  <div class="bg-dim"></div>

  {#if expanded}
    <div class="content">
      <div class="meta">
        <div class="art-box" style={backdropStyle}></div>
        <div class="meta-copy">
          <div class="title" title={title}>{title}</div>
          <div class="subtitle" title={subtitle}>{subtitle}</div>
        </div>
      </div>

      <div class="controls" role="group" aria-label="Radio controls">
        <button class="icon-control" aria-label="Previous channel" data-no-swipe on:click={() => dispatch('previousChannel')}>
          <SkipBack size={18} />
        </button>
        <button
          class="icon-control play"
          aria-label={runtime.isPlaying ? 'Pause playback' : 'Start playback'}
          data-no-swipe
          on:click={() => dispatch('togglePlayback')}
        >
          {#if runtime.isPlaying || runtime.playbackDesired}
            <Pause size={21} />
          {:else}
            <Play size={21} />
          {/if}
        </button>
        <button class="icon-control" aria-label="Next channel" data-no-swipe on:click={() => dispatch('nextChannel')}>
          <SkipForward size={18} />
        </button>
        <button
          class="icon-control quality"
          class:quality-high={isQualityHigh}
          aria-label={qualityAriaLabel}
          aria-pressed={isQualityHigh}
          data-no-swipe
          on:click={() => dispatch('toggleQuality')}
        >
          <AudioLines size={18} />
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
        <label class="volume-wrap">
          <Volume2 size={14} />
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={runtime.volume}
            aria-label="Music volume"
            on:input={(event) => dispatch('setVolume', Number(event.currentTarget.value))}
          />
        </label>
      </div>
    </div>
  {:else}
    <div class="mini-art" style={backdropStyle} aria-hidden="true"></div>
  {/if}
</div>

<style>
  .radio-strip {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    min-height: 82px;
    z-index: 9800;
    overflow: hidden;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 -8px 36px rgba(0, 0, 0, 0.45);
    transition:
      width 0.24s ease,
      height 0.24s ease,
      left 0.24s ease,
      right 0.24s ease,
      bottom 0.24s ease,
      box-shadow 0.24s ease,
      border-color 0.24s ease;
    touch-action: pan-y;
  }

  .radio-strip.collapsed {
    left: 0.75rem;
    right: auto;
    bottom: 0.75rem;
    width: 56px;
    height: 56px;
    min-height: 56px;
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-top: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.45);
  }

  .radio-strip.collapsed .bg-art,
  .radio-strip.collapsed .bg-glow,
  .radio-strip.collapsed .bg-dim {
    display: none;
  }

  .bg-art,
  .bg-glow,
  .bg-dim {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .bg-art {
    background-size: cover;
    background-position: center;
    filter: blur(14px) saturate(1.08);
    transform: scale(1.06);
    opacity: 0.48;
  }

  .bg-glow {
    background:
      radial-gradient(circle at 18% 28%, rgba(var(--radio-glow), 0.34), transparent 52%),
      radial-gradient(circle at 80% 68%, rgba(var(--radio-secondary), 0.26), transparent 56%),
      linear-gradient(130deg, rgba(var(--radio-primary), 0.58), rgba(var(--radio-dim), 0.72));
  }

  .bg-dim {
    background:
      linear-gradient(180deg, rgba(0, 0, 0, 0.18), rgba(var(--radio-dim), 0.86)),
      linear-gradient(100deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0));
  }

  .content {
    position: relative;
    display: grid;
    grid-template-columns: minmax(220px, 1fr) auto minmax(220px, 1fr);
    gap: 0.75rem;
    align-items: center;
    padding: 0.52rem 0.8rem 0.62rem;
  }

  .meta {
    min-width: 0;
    display: inline-flex;
    align-items: center;
    gap: 0.58rem;
  }

  .art-box,
  .mini-art {
    width: 46px;
    height: 46px;
    border: 1px solid rgba(255, 255, 255, 0.28);
    background-color: rgba(0, 0, 0, 0.28);
    background-size: cover;
    background-position: center;
    flex: 0 0 auto;
  }

  .mini-art {
    width: 56px;
    height: 56px;
    border: none;
  }

  .meta-copy {
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
    margin-top: 0.16rem;
    opacity: 0.86;
    font-size: 0.74rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .controls {
    justify-self: center;
    display: inline-flex;
    align-items: center;
    gap: 0.56rem;
  }

  .icon-control {
    appearance: none;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.95);
    cursor: pointer;
    padding: 0.1rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
    transition: transform 0.15s ease, opacity 0.15s ease, color 0.15s ease;
  }

  .icon-control:hover {
    opacity: 0.86;
    transform: translateY(-1px);
  }

  .icon-control.play {
    color: rgba(var(--radio-glow), 1);
  }

  .icon-control.quality {
    color: rgba(214, 224, 243, 0.9);
  }

  .icon-control.quality.quality-high {
    color: rgba(var(--radio-glow), 1);
  }

  .selectors {
    justify-self: end;
    display: inline-flex;
    align-items: center;
    gap: 0.48rem;
  }

  .selectors select {
    appearance: none;
    border: 1px solid rgba(255, 255, 255, 0.25);
    background: rgba(12, 18, 30, 0.62);
    color: inherit;
    min-height: 33px;
    padding: 0 0.5rem;
    max-width: 10rem;
  }

  .volume-wrap {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    border: 1px solid rgba(255, 255, 255, 0.25);
    background: rgba(12, 18, 30, 0.62);
    padding: 0 0.36rem;
    min-height: 33px;
  }

  .volume-wrap input[type='range'] {
    width: 96px;
  }

  .icon-control:focus-visible,
  .selectors select:focus-visible,
  .selectors input[type='range']:focus-visible {
    outline: 2px solid rgba(166, 219, 255, 0.9);
    outline-offset: 2px;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }

  @media (max-width: 960px) {
    .content {
      grid-template-columns: 1fr;
      gap: 0.5rem;
      padding-bottom: calc(0.64rem + env(safe-area-inset-bottom, 0px));
    }

    .meta,
    .controls,
    .selectors {
      justify-self: center;
    }

    .meta {
      text-align: center;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .radio-strip,
    .icon-control {
      transition: none;
    }
  }
</style>

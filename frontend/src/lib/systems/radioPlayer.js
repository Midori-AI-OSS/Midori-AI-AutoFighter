import { writable } from 'svelte/store';

import {
  buildRadioStreamUrl,
  getRadioArt,
  getRadioChannels,
  getRadioCurrent,
  normalizeRadioChannel,
  normalizeRadioQuality,
  resolveRadioArtUrl,
} from './radioApi.js';

const RETRY_DELAYS_MS = [1000, 2000, 4000, 8000, 16000, 30000];
const PLAYING_METADATA_POLL_MS = 5000;
const IDLE_METADATA_POLL_MS = 20000;
const CHANNEL_REFRESH_MS = 60000;
const CHANNEL_FADE_MS = 220;
const PLAY_INTERRUPTED_PATTERN = /play\(\) request was interrupted by a call to pause\(\)/i;

const DEFAULT_STATE = {
  sourceActive: false,
  enabled: false,
  autostart: false,
  channels: ['all'],
  channel: 'all',
  activeQuality: 'medium',
  pendingQuality: null,
  volume: 70,
  playbackDesired: false,
  isPlaying: false,
  connectionState: 'idle',
  statusText: 'Idle',
  currentTrack: null,
  art: null,
  artUrl: '',
  lastError: null,
};

const runtimeStore = writable({ ...DEFAULT_STATE });

let state = { ...DEFAULT_STATE };
let radioAudio = null;
let reconnectTimer = null;
let metadataTimer = null;
let channelTimer = null;
let visibilityBound = false;
let reconnectAttempt = 0;
let lastTrackId = '';
let lastTrackTitle = '';
let started = false;
let playbackIntentId = 0;
let playbackQueue = Promise.resolve();
let metadataRequestId = 0;
let metadataAbortController = null;

function hasAudio() {
  return typeof Audio !== 'undefined';
}

function isDocumentVisible() {
  if (typeof document === 'undefined') return true;
  return document.visibilityState === 'visible';
}

function updateState(patch = {}) {
  state = { ...state, ...patch };
  runtimeStore.set(state);
}

function clampVolume(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return 70;
  return Math.max(0, Math.min(100, Math.round(numeric)));
}

function isPlaybackAbortError(error) {
  if (!error) return false;
  if (error instanceof DOMException && error.name === 'AbortError') return true;
  const name = String(error?.name || '');
  if (name === 'AbortError') return true;
  const message = String(error?.message || error || '');
  return PLAY_INTERRUPTED_PATTERN.test(message);
}

function isRequestAbortError(error) {
  if (!error) return false;
  if (error instanceof DOMException && error.name === 'AbortError') return true;
  return String(error?.name || '') === 'AbortError';
}

function runPlaybackJob(job) {
  const execute = async () => job();
  const scheduled = playbackQueue.then(execute, execute);
  playbackQueue = scheduled.catch(() => undefined);
  return scheduled;
}

function clearReconnectTimer() {
  if (reconnectTimer !== null) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
}

function clearMetadataTimer() {
  if (metadataTimer !== null) {
    clearTimeout(metadataTimer);
    metadataTimer = null;
  }
}

function clearChannelTimer() {
  if (channelTimer !== null) {
    clearTimeout(channelTimer);
    channelTimer = null;
  }
}

function applyVolume() {
  if (!radioAudio) return;
  try {
    radioAudio.volume = clampVolume(state.volume) / 100;
  } catch {
    // ignore audio assignment failures
  }
}

function applyPendingQualityIfNeeded() {
  if (!state.pendingQuality) {
    return state.activeQuality;
  }
  const normalized = normalizeRadioQuality(state.pendingQuality);
  updateState({ activeQuality: normalized, pendingQuality: null });
  return normalized;
}

function desiredPollIntervalMs() {
  if (state.playbackDesired || state.isPlaying) {
    return PLAYING_METADATA_POLL_MS;
  }
  return IDLE_METADATA_POLL_MS;
}

function shouldPollMetadata() {
  return Boolean(state.sourceActive && state.enabled && isDocumentVisible());
}

function shouldRefreshChannels() {
  return Boolean(state.sourceActive && isDocumentVisible());
}

function ensureAudio() {
  if (radioAudio || !hasAudio()) return radioAudio;

  const audio = new Audio();
  audio.preload = 'none';

  audio.addEventListener('playing', () => {
    reconnectAttempt = 0;
    clearReconnectTimer();
    updateState({
      isPlaying: true,
      connectionState: 'playing',
      statusText: 'Live',
      lastError: null,
    });
  });

  audio.addEventListener('pause', () => {
    if (!state.playbackDesired) {
      updateState({ isPlaying: false, connectionState: 'idle', statusText: 'Stopped' });
    }
  });

  const onError = () => {
    if (!state.playbackDesired) return;
    queueReconnect('Stream interrupted.');
  };

  audio.addEventListener('error', onError);
  audio.addEventListener('stalled', onError);
  audio.addEventListener('ended', onError);

  radioAudio = audio;
  applyVolume();
  return radioAudio;
}

function queueReconnect(reason, { immediate = false } = {}) {
  if (!state.playbackDesired) return;
  clearReconnectTimer();
  const idx = Math.min(reconnectAttempt, RETRY_DELAYS_MS.length - 1);
  const delayMs = immediate ? 0 : RETRY_DELAYS_MS[idx];
  reconnectAttempt += 1;
  updateState({
    connectionState: 'retrying',
    statusText: immediate ? 'Reconnecting…' : `${reason} Retrying in ${Math.ceil(delayMs / 1000)}s.`,
    lastError: reason,
    isPlaying: false,
  });

  reconnectTimer = setTimeout(() => {
    reconnectTimer = null;
    void requestStartPlayback({ reasonText: 'Reconnecting…' });
  }, delayMs);
}

function stopPlayback({ preserveDesired = false, rescheduleMetadata = true, invalidateIntent = true } = {}) {
  clearReconnectTimer();
  if (invalidateIntent) {
    playbackIntentId += 1;
  }
  if (!preserveDesired) {
    updateState({ playbackDesired: false });
  }
  reconnectAttempt = 0;
  if (radioAudio) {
    try {
      radioAudio.pause();
      radioAudio.removeAttribute('src');
      radioAudio.load();
    } catch {
      // ignore
    }
  }
  updateState({
    isPlaying: false,
    connectionState: 'idle',
    statusText: preserveDesired ? 'Paused' : 'Stopped',
  });
  if (rescheduleMetadata) {
    scheduleMetadataPoll();
  }
}

async function fadeAudioVolume(target, durationMs) {
  if (!radioAudio || durationMs <= 0) return;
  const start = Number.isFinite(radioAudio.volume) ? radioAudio.volume : 0;
  const end = Math.max(0, Math.min(1, target));
  if (start === end) return;

  const startedAt = (typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now();
  await new Promise((resolve) => {
    const step = (ts) => {
      const now = typeof ts === 'number' ? ts : ((typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now());
      const t = Math.max(0, Math.min(1, (now - startedAt) / durationMs));
      const next = start + ((end - start) * t);
      try {
        radioAudio.volume = next;
      } catch {
        resolve();
        return;
      }
      if (t >= 1) {
        resolve();
      } else if (typeof requestAnimationFrame !== 'undefined') {
        requestAnimationFrame(step);
      } else {
        setTimeout(() => step(), 16);
      }
    };

    if (typeof requestAnimationFrame !== 'undefined') {
      requestAnimationFrame(step);
    } else {
      setTimeout(() => step(), 0);
    }
  });
}

async function startPlaybackInternal({ reasonText = 'Connecting…', intentId = playbackIntentId } = {}) {
  if (intentId !== playbackIntentId) {
    return false;
  }
  if (!state.sourceActive || !state.enabled) {
    stopPlayback({ invalidateIntent: false });
    return false;
  }

  const audio = ensureAudio();
  if (!audio) {
    updateState({
      playbackDesired: false,
      isPlaying: false,
      connectionState: 'error',
      statusText: 'Audio output unavailable',
      lastError: 'Audio output unavailable',
    });
    return false;
  }

  const quality = applyPendingQualityIfNeeded();
  const streamUrl = buildRadioStreamUrl({
    channel: state.channel,
    quality,
    cacheBust: reconnectAttempt > 0,
  });

  updateState({
    playbackDesired: true,
    isPlaying: false,
    connectionState: reconnectAttempt > 0 ? 'retrying' : 'connecting',
    statusText: reasonText,
    lastError: null,
  });

  applyVolume();

  try {
    audio.pause();
    audio.src = streamUrl;
    audio.load();
    await audio.play();

    if (intentId !== playbackIntentId) {
      try {
        audio.pause();
      } catch {
        // ignore stale playback stop failures
      }
      return false;
    }

    scheduleMetadataPoll();
    return true;
  } catch (error) {
    if (error instanceof DOMException && error.name === 'NotAllowedError') {
      updateState({
        playbackDesired: false,
        isPlaying: false,
        connectionState: 'error',
        statusText: 'Playback blocked. Press play to retry.',
        lastError: error.message || 'Playback blocked',
      });
      scheduleMetadataPoll();
      return false;
    }

    if (isPlaybackAbortError(error)) {
      if (intentId === playbackIntentId) {
        updateState({
          isPlaying: false,
          connectionState: state.playbackDesired ? 'connecting' : 'idle',
          statusText: state.playbackDesired ? reasonText : 'Stopped',
          lastError: null,
        });
      }
      scheduleMetadataPoll();
      return false;
    }

    if (intentId !== playbackIntentId) {
      return false;
    }

    queueReconnect(error instanceof Error ? error.message : 'Playback failed');
    scheduleMetadataPoll();
    return false;
  }
}

function requestStartPlayback({ reasonText = 'Connecting…' } = {}) {
  const intentId = ++playbackIntentId;
  return runPlaybackJob(() => startPlaybackInternal({ reasonText, intentId }));
}

async function refreshChannels() {
  if (!shouldRefreshChannels()) {
    return;
  }

  try {
    const payload = await getRadioChannels();
    const entries = Array.isArray(payload?.data?.channels) ? payload.data.channels : [];
    const names = entries
      .map((entry) => normalizeRadioChannel(entry?.name))
      .filter((name) => name !== 'all')
      .filter((name, index, list) => list.indexOf(name) === index)
      .sort((a, b) => a.localeCompare(b));

    const nextChannels = ['all', ...names];
    const selected = nextChannels.includes(state.channel) ? state.channel : 'all';
    updateState({ channels: nextChannels, channel: selected });
  } catch {
    // keep last known channels
  }
}

async function refreshMetadata({ boundaryFollowup = false } = {}) {
  if (!shouldPollMetadata()) {
    return;
  }

  const channel = normalizeRadioChannel(state.channel);
  const requestId = ++metadataRequestId;
  if (metadataAbortController) {
    try {
      metadataAbortController.abort();
    } catch {
      // ignore abort failures
    }
  }
  const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
  metadataAbortController = controller;
  const signal = controller?.signal;

  try {
    const [current, art] = await Promise.all([
      getRadioCurrent(channel, { signal }),
      getRadioArt(channel, { signal }),
    ]);

    if (requestId !== metadataRequestId) {
      return;
    }

    const currentData = current?.data || null;
    const artData = art?.data || null;
    const trackId = String(currentData?.track_id || '').trim();
    const trackTitle = String(currentData?.title || '').trim();

    const boundaryDetected = Boolean(
      (lastTrackId && trackId && lastTrackId !== trackId) ||
      (lastTrackTitle && trackTitle && lastTrackTitle !== trackTitle)
    );

    if (trackId) lastTrackId = trackId;
    if (trackTitle) lastTrackTitle = trackTitle;

    const artUrl = resolveRadioArtUrl(artData?.art_url, channel);

    updateState({
      currentTrack: currentData,
      art: artData,
      artUrl,
      lastError: null,
      statusText: state.isPlaying ? 'Live' : state.statusText,
    });

    if (boundaryDetected) {
      if (state.pendingQuality && state.playbackDesired) {
        await requestStartPlayback({ reasonText: 'Applying quality…' });
      }
      if (!boundaryFollowup) {
        setTimeout(() => {
          void refreshMetadata({ boundaryFollowup: true });
        }, 150);
      }
    }
  } catch (error) {
    if (isRequestAbortError(error) || requestId !== metadataRequestId) {
      return;
    }
    updateState({
      lastError: error instanceof Error ? error.message : 'Metadata refresh failed',
    });
  } finally {
    if (metadataAbortController === controller) {
      metadataAbortController = null;
    }
  }
}

function scheduleChannelRefresh() {
  clearChannelTimer();
  if (!shouldRefreshChannels()) return;
  channelTimer = setTimeout(async () => {
    channelTimer = null;
    await refreshChannels();
    scheduleChannelRefresh();
  }, CHANNEL_REFRESH_MS);
}

function scheduleMetadataPoll() {
  clearMetadataTimer();
  if (!shouldPollMetadata()) return;
  metadataTimer = setTimeout(async () => {
    metadataTimer = null;
    await refreshMetadata();
    scheduleMetadataPoll();
  }, desiredPollIntervalMs());
}

function handleVisibilityChange() {
  if (!isDocumentVisible()) {
    clearMetadataTimer();
    clearChannelTimer();
    return;
  }
  if (state.sourceActive) {
    void refreshChannels();
    void refreshMetadata();
  }
  scheduleChannelRefresh();
  scheduleMetadataPoll();
}

function ensureVisibilityBinding() {
  if (visibilityBound || typeof document === 'undefined') return;
  document.addEventListener('visibilitychange', handleVisibilityChange);
  visibilityBound = true;
}

function maybeAutostart() {
  if (!state.sourceActive || !state.enabled || !state.autostart) return;
  if (state.playbackDesired || state.isPlaying) return;
  void requestStartPlayback();
}

export function initializeRadioPlayer(config = {}) {
  if (started) {
    updateRadioSettings(config);
    return runtimeStore;
  }

  started = true;
  ensureVisibilityBinding();
  updateState({
    ...DEFAULT_STATE,
    sourceActive: Boolean(config.sourceActive),
    enabled: Boolean(config.enabled),
    autostart: Boolean(config.autostart),
    channel: normalizeRadioChannel(config.channel),
    activeQuality: normalizeRadioQuality(config.quality),
    volume: clampVolume(config.volume),
  });
  applyVolume();
  void refreshChannels();
  void refreshMetadata();
  scheduleChannelRefresh();
  scheduleMetadataPoll();
  maybeAutostart();

  return runtimeStore;
}

export function updateRadioSettings(config = {}) {
  const nextChannel = normalizeRadioChannel(config.channel ?? state.channel);
  const nextQuality = normalizeRadioQuality(config.quality ?? state.activeQuality);
  const nextVolume = clampVolume(config.volume ?? state.volume);
  const nextEnabled = Boolean(config.enabled ?? state.enabled);
  const nextAutostart = Boolean(config.autostart ?? state.autostart);

  const channelChanged = nextChannel !== state.channel;
  const qualityChanged = nextQuality !== state.activeQuality;
  const enabledChanged = nextEnabled !== state.enabled;

  updateState({
    enabled: nextEnabled,
    autostart: nextAutostart,
    channel: nextChannel,
    volume: nextVolume,
  });

  if (qualityChanged) {
    if (state.playbackDesired || state.isPlaying) {
      updateState({ pendingQuality: nextQuality });
    } else {
      updateState({ activeQuality: nextQuality, pendingQuality: null });
    }
  }

  applyVolume();

  if (!nextEnabled) {
    stopPlayback();
  } else if (enabledChanged && state.sourceActive && state.autostart) {
    void requestStartPlayback();
  }

  if (channelChanged) {
    if (state.playbackDesired || state.isPlaying) {
      void switchChannelWithFade(nextChannel);
    }
    void refreshMetadata();
  }

  scheduleMetadataPoll();
  scheduleChannelRefresh();
}

async function switchChannelWithFade(channel) {
  const intentId = ++playbackIntentId;
  return runPlaybackJob(async () => {
    if (intentId !== playbackIntentId) {
      return false;
    }

    if (!radioAudio || !state.playbackDesired) {
      return startPlaybackInternal({ reasonText: 'Switching channel…', intentId });
    }

    updateState({ connectionState: 'connecting', statusText: `Switching channel to ${channel}…` });
    await fadeAudioVolume(0, CHANNEL_FADE_MS);

    if (intentId !== playbackIntentId) {
      return false;
    }

    const startedPlayback = await startPlaybackInternal({ reasonText: 'Switching channel…', intentId });
    if (!startedPlayback) {
      return false;
    }

    applyVolume();
    await fadeAudioVolume(clampVolume(state.volume) / 100, CHANNEL_FADE_MS);
    void refreshMetadata();
    return true;
  });
}

export function setRadioSourceActive(active) {
  const next = Boolean(active);
  if (next === state.sourceActive) return;
  updateState({ sourceActive: next });

  if (!next) {
    stopPlayback();
  } else {
    void refreshChannels();
    void refreshMetadata();
    maybeAutostart();
  }

  scheduleChannelRefresh();
  scheduleMetadataPoll();
}

export async function toggleRadioPlayback() {
  if (state.playbackDesired || state.isPlaying) {
    stopPlayback();
    return false;
  }
  return requestStartPlayback();
}

export function resumeRadioPlayback() {
  if (!state.playbackDesired) return;
  if (!state.sourceActive || !state.enabled) return;
  if (state.isPlaying) return;
  void requestStartPlayback({ reasonText: 'Resuming…' });
}

export function stepRadioChannel(direction) {
  const dir = Number(direction);
  if (!Number.isFinite(dir) || dir === 0) {
    return state.channel;
  }

  const channels = Array.isArray(state.channels) && state.channels.length > 0 ? state.channels : ['all'];
  const current = channels.indexOf(state.channel);
  const index = current >= 0 ? current : 0;
  const nextIndex = (index + (dir > 0 ? 1 : -1) + channels.length) % channels.length;
  const nextChannel = channels[nextIndex] || 'all';

  updateState({ channel: nextChannel });
  if (state.playbackDesired || state.isPlaying) {
    void switchChannelWithFade(nextChannel);
  }
  void refreshMetadata();
  return nextChannel;
}

export function setRadioChannel(channel) {
  const normalized = normalizeRadioChannel(channel);
  if (normalized === state.channel) return normalized;
  updateState({ channel: normalized });
  if (state.playbackDesired || state.isPlaying) {
    void switchChannelWithFade(normalized);
  }
  void refreshMetadata();
  return normalized;
}

export function toggleRadioQualityHighMedium() {
  const target = (state.pendingQuality || state.activeQuality) === 'high' ? 'medium' : 'high';
  if (state.playbackDesired || state.isPlaying) {
    updateState({ pendingQuality: target, statusText: `Quality queued (${target})` });
  } else {
    updateState({ activeQuality: target, pendingQuality: null });
  }
  return target;
}

export function setRadioVolume(volume) {
  const clamped = clampVolume(volume);
  updateState({ volume: clamped });
  applyVolume();
  return clamped;
}

export function getRadioRuntimeSnapshot() {
  return { ...state };
}

export function destroyRadioPlayer() {
  clearReconnectTimer();
  clearMetadataTimer();
  clearChannelTimer();
  if (metadataAbortController) {
    try {
      metadataAbortController.abort();
    } catch {
      // ignore abort failures
    }
    metadataAbortController = null;
  }
  stopPlayback({ rescheduleMetadata: false });

  if (visibilityBound && typeof document !== 'undefined') {
    document.removeEventListener('visibilitychange', handleVisibilityChange);
    visibilityBound = false;
  }

  if (radioAudio) {
    try {
      radioAudio.pause();
      radioAudio.removeAttribute('src');
      radioAudio.load();
    } catch {
      // ignore
    }
    radioAudio = null;
  }

  reconnectAttempt = 0;
  lastTrackId = '';
  lastTrackTitle = '';
  playbackIntentId = 0;
  playbackQueue = Promise.resolve();
  metadataRequestId = 0;
  started = false;
  state = { ...DEFAULT_STATE };
  runtimeStore.set(state);
}

export { runtimeStore as radioRuntimeStore };

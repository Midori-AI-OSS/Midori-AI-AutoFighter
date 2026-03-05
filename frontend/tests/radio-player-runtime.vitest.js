import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const { getRadioChannels, getRadioCurrent, getRadioArt, resolveRadioArtUrl } = vi.hoisted(() => ({
  getRadioChannels: vi.fn(),
  getRadioCurrent: vi.fn(),
  getRadioArt: vi.fn(),
  resolveRadioArtUrl: vi.fn(),
}));

vi.mock('../src/lib/systems/radioApi.js', () => ({
  buildRadioStreamUrl: ({ channel = 'all', quality = 'medium' } = {}) => `https://radio.midori-ai.xyz/radio/v1/stream?channel=${channel}&q=${quality}`,
  getRadioChannels,
  getRadioCurrent,
  getRadioArt,
  normalizeRadioChannel: (value) => String(value || 'all').trim().toLowerCase() || 'all',
  normalizeRadioQuality: (value) => {
    const next = String(value || '').trim().toLowerCase();
    return ['low', 'medium', 'high'].includes(next) ? next : 'medium';
  },
  resolveRadioArtUrl,
}));

import {
  destroyRadioPlayer,
  getRadioRuntimeSnapshot,
  initializeRadioPlayer,
  setRadioChannel,
  toggleRadioPlayback,
} from '../src/lib/systems/radioPlayer.js';

function defer() {
  let resolve;
  let reject;
  const promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

async function flush() {
  await Promise.resolve();
  await Promise.resolve();
}

describe('radioPlayer runtime guards', () => {
  let nextPlayImpl;

  beforeEach(() => {
    destroyRadioPlayer();
    nextPlayImpl = () => Promise.resolve();

    globalThis.Audio = class {
      constructor() {
        this.preload = 'none';
        this.src = '';
        this.volume = 1;
        this._listeners = new Map();
      }

      addEventListener(name, handler) {
        const list = this._listeners.get(name) || [];
        list.push(handler);
        this._listeners.set(name, list);
      }

      pause() {}

      load() {}

      removeAttribute(attr) {
        if (attr === 'src') this.src = '';
      }

      play() {
        return nextPlayImpl();
      }
    };

    getRadioChannels.mockReset().mockResolvedValue({ data: { channels: [{ name: 'all' }, { name: 'jazz' }] } });
    getRadioCurrent.mockReset().mockResolvedValue({ data: { title: 'Track One', track_id: 'track-1' } });
    getRadioArt.mockReset().mockResolvedValue({ data: { art_url: '/art-1' } });
    resolveRadioArtUrl.mockReset().mockImplementation((raw) => String(raw || ''));
  });

  afterEach(() => {
    destroyRadioPlayer();
    delete globalThis.Audio;
  });

  it('treats interrupted play AbortError as expected cancellation', async () => {
    initializeRadioPlayer({
      sourceActive: true,
      enabled: true,
      autostart: false,
      channel: 'all',
      quality: 'medium',
      volume: 70,
    });
    await flush();

    nextPlayImpl = () => Promise.reject(new DOMException('The play() request was interrupted by a call to pause().', 'AbortError'));

    const started = await toggleRadioPlayback();
    expect(started).toBe(false);

    const snapshot = getRadioRuntimeSnapshot();
    expect(snapshot.lastError).toBeNull();
    expect(snapshot.statusText).not.toContain('Retrying');
    expect(snapshot.connectionState).not.toBe('error');
  });

  it('keeps latest metadata response when older request resolves afterward', async () => {
    const firstCurrent = defer();
    const firstArt = defer();
    const secondCurrent = defer();
    const secondArt = defer();

    let currentCalls = 0;
    getRadioCurrent.mockImplementation(() => {
      currentCalls += 1;
      return currentCalls === 1 ? firstCurrent.promise : secondCurrent.promise;
    });

    let artCalls = 0;
    getRadioArt.mockImplementation(() => {
      artCalls += 1;
      return artCalls === 1 ? firstArt.promise : secondArt.promise;
    });

    initializeRadioPlayer({
      sourceActive: true,
      enabled: true,
      autostart: false,
      channel: 'all',
      quality: 'medium',
      volume: 70,
    });
    await flush();

    setRadioChannel('jazz');
    await flush();

    secondCurrent.resolve({ data: { title: 'Newest Track', track_id: 'track-new' } });
    secondArt.resolve({ data: { art_url: '/new-art' } });
    await flush();
    await flush();

    firstCurrent.resolve({ data: { title: 'Old Track', track_id: 'track-old' } });
    firstArt.resolve({ data: { art_url: '/old-art' } });
    await flush();
    await flush();

    const snapshot = getRadioRuntimeSnapshot();
    expect(snapshot.currentTrack?.title).toBe('Newest Track');
    expect(snapshot.currentTrack?.track_id).toBe('track-new');
    expect(snapshot.artUrl).toBe('/new-art');
  });
});

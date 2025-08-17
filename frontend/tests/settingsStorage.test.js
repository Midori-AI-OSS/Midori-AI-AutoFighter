import { describe, expect, test, beforeEach } from 'bun:test';
import { loadSettings, saveSettings, clearSettings } from '../src/lib/settingsStorage.js';

function mockStorage() {
  let store = {};
  return {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => {
      store[k] = String(v);
    },
    removeItem: (k) => {
      delete store[k];
    },
    clear: () => {
      store = {};
    }
  };
}

beforeEach(() => {
  global.localStorage = mockStorage();
  localStorage.clear();
});

describe('settings storage', () => {
  test('persists framerate selection', () => {
    saveSettings({ framerate: 30 });
    const result = loadSettings();
    expect(result.framerate).toBe(30);
  });

  test('merges settings and normalizes numeric values', () => {
    saveSettings({ musicVolume: 10, framerate: '60' });
    saveSettings({ sfxVolume: 20 });
    const result = loadSettings();
    expect(result.musicVolume).toBe(10);
    expect(result.sfxVolume).toBe(20);
    expect(result.framerate).toBe(60);
    expect(typeof result.framerate).toBe('number');
  });

  test('clearSettings removes stored values', () => {
    saveSettings({ sfxVolume: 40 });
    clearSettings();
    const result = loadSettings();
    expect(result).toEqual({});
  });
});

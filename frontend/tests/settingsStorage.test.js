import { describe, expect, test, beforeEach } from 'bun:test';
import { loadSettings, saveSettings } from '../src/lib/settingsStorage.js';

function mockStorage() {
  let store = {};
  return {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => {
      store[k] = String(v);
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
});

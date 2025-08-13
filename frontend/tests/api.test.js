import { describe, expect, test, mock } from 'bun:test';
import {
  startRun,
  updateParty,
  fetchMap,
  getPlayers,
  battleRoom,
  shopRoom,
  restRoom,
  getPlayerConfig,
  savePlayerConfig,
  getGacha,
  pullGacha,
  setAutoCraft
} from '../src/lib/api.js';

// Helper to mock fetch
function createFetch(response) {
  return mock(async () => ({ json: async () => response }));
}

describe('api calls', () => {
  test('startRun returns run data', async () => {
    global.fetch = createFetch({ run_id: '123', map: [] });
    const result = await startRun(['player']);
    expect(result).toEqual({ run_id: '123', map: [] });
  });

  test('updateParty sends party', async () => {
    global.fetch = createFetch({ status: 'ok' });
    const result = await updateParty('abc', ['sample_player']);
    expect(result).toEqual({ status: 'ok' });
  });

  test('fetchMap retrieves map', async () => {
    global.fetch = createFetch({ map: ['start'] });
    const result = await fetchMap('abc');
    expect(result).toEqual({ map: ['start'] });
  });

  test('getPlayers retrieves roster', async () => {
    global.fetch = createFetch({ players: [{ id: 'sample_player', owned: true }] });
    const result = await getPlayers();
    expect(result).toEqual({ players: [{ id: 'sample_player', owned: true }] });
  });

  test('battleRoom posts action', async () => {
    global.fetch = createFetch({ result: 'battle', party: [], foes: [] });
    const result = await battleRoom('abc', 'attack');
    expect(result).toEqual({ result: 'battle', party: [], foes: [] });
  });

  test('shopRoom posts action', async () => {
    global.fetch = createFetch({ result: 'shop', party: [], foes: [] });
    const result = await shopRoom('abc', 'buy');
    expect(result).toEqual({ result: 'shop', party: [], foes: [] });
  });

  test('restRoom posts action', async () => {
    global.fetch = createFetch({ result: 'rest', party: [], foes: [] });
    const result = await restRoom('abc', 'sleep');
    expect(result).toEqual({ result: 'rest', party: [], foes: [] });
  });

  test('getPlayerConfig fetches editor data', async () => {
    const payload = { pronouns: 'they', damage_type: 'Fire', hp: 0, attack: 0, defense: 0 };
    global.fetch = createFetch(payload);
    const result = await getPlayerConfig();
    expect(result).toEqual(payload);
  });

  test('savePlayerConfig posts editor data', async () => {
    global.fetch = createFetch({ status: 'ok' });
    const result = await savePlayerConfig({ pronouns: 'they', damage_type: 'Fire', hp: 1, attack: 2, defense: 3 });
    expect(result).toEqual({ status: 'ok' });
  });

  test('getGacha retrieves state', async () => {
    global.fetch = createFetch({ pity: 0, items: {}, players: [] });
    const result = await getGacha();
    expect(result).toEqual({ pity: 0, items: {}, players: [] });
  });

  test('pullGacha posts count', async () => {
    global.fetch = createFetch({ results: [], pity: 0 });
    const result = await pullGacha(5);
    expect(result).toEqual({ results: [], pity: 0 });
  });

  test('setAutoCraft posts flag', async () => {
    global.fetch = createFetch({ status: 'ok', auto_craft: true });
    const result = await setAutoCraft(true);
    expect(result).toEqual({ status: 'ok', auto_craft: true });
  });
});

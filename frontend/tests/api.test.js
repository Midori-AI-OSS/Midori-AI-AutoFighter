import { describe, expect, test, mock } from 'bun:test';
import {
  startRun,
  updateParty,
  fetchMap,
  getPlayers,
  roomAction,
  getPlayerConfig,
  savePlayerConfig,
  getGacha,
  pullGacha,
  setAutoCraft,
  chooseCard,
  wipeData
} from '../src/lib/api.js';

// Helper to mock fetch
function createFetch(response, ok = true, status = 200) {
  return mock(async () => ({ ok, status, json: async () => response }));
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
    const payload = { map: { rooms: ['start'], current: 0, battle: false } };
    global.fetch = createFetch(payload);
    const result = await fetchMap('abc');
    expect(result).toEqual(payload);
  });

  test('getPlayers retrieves roster', async () => {
    global.fetch = createFetch({ players: [{ id: 'sample_player', owned: true }] });
    const result = await getPlayers();
    expect(result).toEqual({ players: [{ id: 'sample_player', owned: true }] });
  });

  test('roomAction posts action', async () => {
    global.fetch = createFetch({ result: 'battle', party: [], foes: [] });
    const result = await roomAction('abc', 'battle', 'attack');
    expect(result).toEqual({ result: 'battle', party: [], foes: [] });
  });

  test('roomAction throws on HTTP error', async () => {
    global.fetch = createFetch({}, false, 500);
    await expect(roomAction('abc', 'battle', 'attack')).rejects.toThrow('HTTP error 500');
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

  test('chooseCard posts card selection', async () => {
    const payload = { card: { id: 'c1', name: 'Card', stars: 1 }, cards: ['c1'] };
    global.fetch = createFetch(payload);
    const result = await chooseCard('abc', 'c1');
    expect(result).toEqual(payload);
  });

  test('wipeData posts wipe and returns status', async () => {
    global.fetch = createFetch({ status: 'wiped' });
    const result = await wipeData();
    expect(result).toEqual({ status: 'wiped' });
  });

  test('wipeData throws on HTTP error', async () => {
    global.fetch = createFetch({}, false, 500);
    await expect(wipeData()).rejects.toThrow('HTTP error 500');
  });
});

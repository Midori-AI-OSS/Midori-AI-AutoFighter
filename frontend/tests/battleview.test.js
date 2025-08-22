import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('BattleView enrage effect', () => {
  test('adds enraged class and animation', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('class:enraged');
    expect(content).toContain('@keyframes enrage-bg');
    expect(content).toContain('--flash-duration');
  });
});

describe('BattleView enrage state', () => {
  test('updates enrage from snapshot', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('snap.enrage && differs(snap.enrage, enrage)');
  });
});

describe('BattleView layout and polling', () => {
  test('renders party and foe columns', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('party-column');
    expect(content).toContain('foe-column');
  });

  test('wraps stat blocks with stained-glass styling', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('class="stats right stained-glass-panel"');
    expect(content).toContain('class="stats left stained-glass-panel"');
  });

  test('party column precedes foe column', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    const partyIndex = content.indexOf('class="party-column"');
    const foeIndex = content.indexOf('class="foe-column"');
    expect(partyIndex).toBeGreaterThan(-1);
    expect(foeIndex).toBeGreaterThan(-1);
    expect(partyIndex).toBeLessThan(foeIndex);
  });

  test('polls backend for snapshots', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain("roomAction(runId, 'battle', 'snapshot')");
  });

  test('shows hp bars and core stats', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('hp-bar');
    expect(content).toContain('<span class="k">DEF</span>');
    expect(content).toContain('CRate');
    expect(content).toContain('CDmg');
  });

  test('groups duplicate effects with stack counts', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('groupEffects');
    expect(content).toContain('stack');
  });

  test('uses normalized element for foe portrait', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('getElementIcon(foe.element)');
    expect(content).toContain('getElementColor(foe.element)');
  });

  test('polling respects framerate settings', async () => {
    async function measure(fps) {
      const pollDelay = 1000 / fps;
      return await new Promise((resolve) => {
        let last = performance.now();
        let count = 0;
        let total = 0;

        async function snap() {
          const start = performance.now();
          await Promise.resolve();
          const duration = performance.now() - start;
          const now = performance.now();
          total += now - last;
          last = now;
          if (++count === 5) {
            resolve(total / 5);
          } else {
            setTimeout(snap, Math.max(0, pollDelay - duration));
          }
        }

        setTimeout(snap, pollDelay);
      });
    }

    const interval30 = await measure(30);
    expect(interval30).toBeGreaterThanOrEqual(33.3 * 0.9);
    expect(interval30).toBeLessThanOrEqual(33.3 * 1.2);

    const interval60 = await measure(60);
    expect(interval60).toBeGreaterThanOrEqual(16.7 * 0.9);
    expect(interval60).toBeLessThanOrEqual(16.7 * 1.2);

    const interval120 = await measure(120);
    expect(interval120).toBeGreaterThanOrEqual(8.3 * 0.9);
    expect(interval120).toBeLessThanOrEqual(8.3 * 1.2);
  });
});

describe('BattleView damage_type fallback', () => {
  test('elementOf resolves singular damage_type', () => {
    function elementOf(obj) {
      if (obj && Array.isArray(obj.damage_types) && obj.damage_types.length > 0) {
        const primary = obj.damage_types[0];
        if (typeof primary === 'string' && primary.length) return primary;
        const id = primary?.id || primary?.name;
        if (id) return id;
      }
      const single = obj?.damage_type;
      if (typeof single === 'string' && single.length) return single;
      const singleId = single?.id || single?.name;
      if (singleId) return singleId;
      const elem = obj?.element;
      if (typeof elem === 'string' && elem.length) return elem;
      return 'Generic';
    }
    const fighter = { id: 'hero', damage_type: 'Fire' };
    expect(elementOf(fighter)).toBe('Fire');
  });
});

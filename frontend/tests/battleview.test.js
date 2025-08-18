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

describe('BattleView layout and polling', () => {
  test('renders party and foe columns', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('party-column');
    expect(content).toContain('foe-column');
  });

  test('polls backend for snapshots', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain("roomAction(runId, 'battle', 'snapshot')");
  });

  test('shows hp bars and core stats', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('hp-bar');
    expect(content).toContain('DEF {');
    expect(content).toContain('CRIT');
  });
});

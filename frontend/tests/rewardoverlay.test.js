import { readFileSync } from 'fs';
import { join } from 'path';
import { describe, test, expect } from 'bun:test';

describe('reward overlay assets', () => {
  test('loader pulls art from codex downloads', () => {
    const loader = readFileSync(join(import.meta.dir, '../src/lib/rewardLoader.js'), 'utf8');
    expect(loader).toContain('.codex/downloads/card-art');
    expect(loader).toContain('.codex/downloads/relics');
  });

  test('overlay lists cards', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/RewardOverlay.svelte'), 'utf8');
    expect(content).toContain('Choose a Card');
    expect(content).toContain('select(\'card\'');
    expect(content).toContain('MenuPanel');
  });
});

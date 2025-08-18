import { readFileSync } from 'fs';
import { join } from 'path';
import { describe, test, expect } from 'bun:test';

describe('reward overlay assets', () => {
  test('loader pulls art from frontend assets', () => {
    const loader = readFileSync(join(import.meta.dir, '../src/lib/rewardLoader.js'), 'utf8');
    expect(loader).toContain('./assets/cards/gray');
    expect(loader).not.toContain('.codex/downloads');
  });

  test('overlay provides confirm flow', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/RewardOverlay.svelte'), 'utf8');
    expect(content).toContain('Choose a Card');
    expect(content).toContain('Confirm');
    expect(content).toContain('selected = { type');
  });
});

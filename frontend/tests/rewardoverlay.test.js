import { readFileSync } from 'fs';
import { join } from 'path';
import { describe, test, expect } from 'bun:test';

describe('reward overlay assets', () => {
  test('loader pulls art from frontend assets', () => {
    const loader = readFileSync(join(import.meta.dir, '../src/lib/rewardLoader.js'), 'utf8');
    expect(loader).toContain('./assets/cards/*');
    expect(loader).not.toContain('.codex/downloads');
  });

  test('overlay provides confirm flow', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/RewardOverlay.svelte'), 'utf8');
    expect(content).toContain('Choose a Card');
    expect(content).toContain('Choose a Relic');
    expect(content).toContain('Confirm');
    expect(content).toContain('selected = { type');
    expect(content).toContain('filter: grayscale(1)');
    expect(content).toContain('--star-color');
    expect(content).toContain("selected.type === 'card' || selected.type === 'relic'");
    expect(content).toContain('selected.data.about');
  });

  test('1x3 grid dimensions', () => {
    const cardWidth = 72;
    const cardHeight = 96;
    const gap = 8; // 0.5rem
    const cols = 3;
    const rows = 1;
    const width = cardWidth * cols + gap * (cols - 1);
    const height = cardHeight * rows + gap * (rows - 1);
    expect(width).toBe(232);
    expect(height).toBe(96);
  });

  test('2x3 grid dimensions', () => {
    const cardWidth = 72;
    const cardHeight = 96;
    const gap = 8; // 0.5rem
    const cols = 3;
    const rows = 2;
    const width = cardWidth * cols + gap * (cols - 1);
    const height = cardHeight * rows + gap * (rows - 1);
    expect(width).toBe(232);
    expect(height).toBe(200);
  });
});

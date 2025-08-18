import { readFileSync } from 'fs';
import { join } from 'path';
import { describe, test, expect } from 'bun:test';

describe('shop menu', () => {
  test('shows currency and buy flow', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/ShopMenu.svelte'), 'utf8');
    expect(content).toContain('<Coins');
    expect(content).toContain('on:click={() => buy(item)}');
    expect(content).toContain('Reroll');
    expect(content).toContain('Leave');
  });
});

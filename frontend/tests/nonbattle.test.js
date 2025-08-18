import { readFileSync } from 'fs';
import { join } from 'path';
import { describe, test, expect } from 'bun:test';

describe('non-battle room routing', () => {
  test('renders shop and rest overlays', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain("roomData && roomData.result === 'shop'");
    expect(content).toContain('ShopMenu');
    expect(content).toContain("roomData && roomData.result === 'rest'");
    expect(content).toContain('RestRoom');
  });
});

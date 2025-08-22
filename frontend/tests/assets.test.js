import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

function pngSize(path) {
  const buf = readFileSync(path);
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

describe('asset placeholders', () => {
  test('item icons exist for each damage type', () => {
    const types = ['dark', 'fire', 'ice', 'light', 'lightning', 'wind', 'generic'];
    for (const t of types) {
      const name = t === 'generic' ? 'generic1.png' : `${t}1.png`;
      const file = join(import.meta.dir, `../src/lib/assets/items/${t}/${name}`);
      const { width, height } = pngSize(file);
      expect(width).toBeGreaterThan(0);
      expect(height).toBeGreaterThan(0);
    }
  });

  test('relic placeholders cover all star ranks', () => {
    const ranks = ['1star', '2star', '3star', '4star', '5star', 'fallback'];
    for (const r of ranks) {
      const relic = join(import.meta.dir, `../src/lib/assets/relics/${r}/placeholder.png`);
      const { width, height } = pngSize(relic);
      expect(width).toBeGreaterThan(0);
      expect(height).toBeGreaterThan(0);
    }
  });

  test('card placeholder exists', () => {
    const card = join(import.meta.dir, '../src/lib/assets/cards/gray/bg_attack_default_gray.png');
    const { width, height } = pngSize(card);
    expect(width).toBeGreaterThan(0);
    expect(height).toBeGreaterThan(0);
  });
});

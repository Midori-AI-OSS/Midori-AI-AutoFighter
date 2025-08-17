import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('BattleView component', () => {
  test('uses random background and element-colored party icons', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/BattleView.svelte'), 'utf8');
    expect(content).toContain('getRandomBackground');
    expect(content).toContain('background-image');
    expect(content).toContain('getElementColor(member.element)');
  });
});

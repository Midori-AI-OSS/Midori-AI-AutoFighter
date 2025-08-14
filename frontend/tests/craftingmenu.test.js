import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('CraftingMenu component', () => {
  test('has auto-craft toggle and craft button', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/CraftingMenu.svelte'), 'utf8');
    expect(content).toContain('Auto-craft');
    expect(content).toContain('Craft');
  });
});

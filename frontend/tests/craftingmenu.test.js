import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';
import { stackItems, formatName } from '../src/lib/craftingUtils.js';

describe('CraftingMenu component', () => {
  test('has auto-craft toggle and craft button', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/CraftingMenu.svelte'), 'utf8');
    expect(content).toContain('Auto-craft');
    expect(content).toContain('Craft');
  });

  test('renders item icons with star outlines and fallback', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/CraftingMenu.svelte'), 'utf8');
    expect(content).toContain('item-icon');
    expect(content).toContain('--star-color');
    expect(content).toContain('on:error={onIconError}');
    expect(content).toContain('fallbackIcon');
  });

  test('includes detail panel placeholder', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/CraftingMenu.svelte'), 'utf8');
    expect(content).toContain('Select an item');
    expect(content).toContain('content');
  });

  test('stacks duplicate items and formats names', () => {
    const stacked = stackItems(['ice_4', 'ice_4', 'fire_2']);
    expect(stacked).toEqual({ ice_4: 2, fire_2: 1 });
    expect(formatName('ice_4')).toBe('Ice ★★★★');
    expect(formatName('lightning_3')).toBe('Lightning ★★★');
    expect(formatName('generic_2')).toBe('Generic ★★');
    expect(formatName('ticket')).toBe('Ticket');
  });
});

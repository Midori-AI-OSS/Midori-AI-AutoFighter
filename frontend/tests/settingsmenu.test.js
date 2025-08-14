import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('SettingsMenu component', () => {
  test('renders volume sliders and pause toggle', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/SettingsMenu.svelte'), 'utf8');
    expect(content).toContain('SFX Volume');
    expect(content).toContain('Music Volume');
    expect(content).toContain('Pause on Stat Screen');
  });
});

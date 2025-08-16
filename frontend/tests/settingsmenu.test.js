import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('SettingsMenu component', () => {
  test('renders volume sliders and headings', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/SettingsMenu.svelte'), 'utf8');
    expect(content).toContain('SFX Volume');
    expect(content).toContain('Music Volume');
    expect(content).toContain('Voice Volume');
    expect(content).toContain('<h4>Audio</h4>');
    expect(content).toContain('<h4>System</h4>');
    expect(content).toContain('<h4>Gameplay</h4>');
  });
});

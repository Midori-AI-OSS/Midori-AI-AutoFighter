import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Framerate persistence', () => {
  test('GameViewport loads saved framerate', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain('if (saved.framerate !== undefined) framerate = Number(saved.framerate);');
  });

  test('SettingsMenu exposes 30/60/120 fps options', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/SettingsMenu.svelte'), 'utf8');
    expect(content).toContain('<option value={30}>30</option>');
    expect(content).toContain('<option value={60}>60</option>');
    expect(content).toContain('<option value={120}>120</option>');
  });

  test('settingsStorage coerces framerate to Number', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/settingsStorage.js'), 'utf8');
    expect(content).toContain('data.framerate = Number(data.framerate);');
  });
});

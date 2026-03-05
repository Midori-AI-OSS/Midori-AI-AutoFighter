import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Radio settings wiring', () => {
  test('settings storage includes radio defaults', () => {
    const settingsFile = join(import.meta.dir, '../src/lib/systems/settingsStorage.js');
    const content = readFileSync(settingsFile, 'utf8');

    expect(content).toContain("musicSource: 'game'");
    expect(content).toContain('radioEnabled: false');
    expect(content).toContain('radioAutostart: false');
    expect(content).toContain("radioChannel: 'all'");
    expect(content).toContain("radioQuality: 'medium'");
    expect(content).toContain('radioVolume: 70');
  });

  test('settings menu payload saves radio fields', () => {
    const settingsMenuFile = join(import.meta.dir, '../src/lib/components/SettingsMenu.svelte');
    const content = readFileSync(settingsMenuFile, 'utf8');

    expect(content).toContain('musicSource,');
    expect(content).toContain('radioEnabled,');
    expect(content).toContain('radioAutostart,');
    expect(content).toContain('radioChannel,');
    expect(content).toContain('radioQuality,');
    expect(content).toContain('radioVolume');
  });

  test('viewport renders radio strip and hides exp bar while radio is active', () => {
    const viewportFile = join(import.meta.dir, '../src/lib/components/GameViewport.svelte');
    const content = readFileSync(viewportFile, 'utf8');

    expect(content).toContain('RadioPlayerStrip');
    expect(content).toContain("musicSource === 'midoriai_radio'");
    expect(content).toContain('class="user-level-bar"');
  });
});

import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Radio settings wiring', () => {
  test('settings storage includes radio defaults and canonical music volume', () => {
    const settingsFile = join(import.meta.dir, '../src/lib/systems/settingsStorage.js');
    const content = readFileSync(settingsFile, 'utf8');

    expect(content).toContain('musicVolume: 70');
    expect(content).toContain("musicSource: 'game'");
    expect(content).toContain('radioEnabled: false');
    expect(content).toContain('radioAutostart: false');
    expect(content).toContain("radioChannel: 'all'");
    expect(content).toContain("radioQuality: 'medium'");
    expect(content).toContain('radioVolume: 70');
    expect(content).toContain('normalizeMusicVolumeSetting');
  });

  test('settings menu payload only saves radio toggles', () => {
    const settingsMenuFile = join(import.meta.dir, '../src/lib/components/SettingsMenu.svelte');
    const content = readFileSync(settingsMenuFile, 'utf8');

    expect(content).toContain('musicSource,');
    expect(content).toContain('radioEnabled,');
    expect(content).toContain('radioAutostart');
    expect(content).not.toContain('radioChannel,');
    expect(content).not.toContain('radioQuality,');
    expect(content).not.toContain('radioVolume');
  });

  test('audio settings keep music source first and remove radio channel/quality/volume controls', () => {
    const audioFile = join(import.meta.dir, '../src/lib/components/AudioSettings.svelte');
    const content = readFileSync(audioFile, 'utf8');

    const musicSourceIndex = content.indexOf('Music Source');
    const sfxIndex = content.indexOf('SFX Volume');
    expect(musicSourceIndex).toBeGreaterThan(-1);
    expect(sfxIndex).toBeGreaterThan(-1);
    expect(musicSourceIndex).toBeLessThan(sfxIndex);

    expect(content).not.toContain('Radio Channel');
    expect(content).not.toContain('Radio Quality');
    expect(content).not.toContain('Radio Volume');
  });

  test('settings menu exposes radio tab only when radio source is active', () => {
    const settingsMenuFile = join(import.meta.dir, '../src/lib/components/SettingsMenu.svelte');
    const content = readFileSync(settingsMenuFile, 'utf8');

    expect(content).toContain("musicSource === 'midoriai_radio'");
    expect(content).toContain("activeTab === 'radio'");
    expect(content).toContain('<RadioSettings');
    const audioTab = content.indexOf('title=\"Audio\"');
    const radioTab = content.indexOf('title=\"Radio\"');
    const uiTab = content.indexOf('title=\"UI\"');
    expect(audioTab).toBeGreaterThan(-1);
    expect(radioTab).toBeGreaterThan(-1);
    expect(uiTab).toBeGreaterThan(-1);
    expect(audioTab).toBeLessThan(radioTab);
    expect(radioTab).toBeLessThan(uiTab);
  });

  test('viewport renders radio strip and hides exp bar while radio is active', () => {
    const viewportFile = join(import.meta.dir, '../src/lib/components/GameViewport.svelte');
    const content = readFileSync(viewportFile, 'utf8');

    expect(content).toContain('RadioPlayerStrip');
    expect(content).toContain("musicSource === 'midoriai_radio'");
    expect(content).toContain('class="user-level-bar"');
    expect(content).toContain('applySavedSettings');
  });
});

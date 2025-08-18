import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('GameViewport battle lock', () => {
  test('disables menu buttons during battle', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain('battleActive');
    expect(content).toContain('disabled={item.disabled}');
  });

  test('shows battle icon during combat', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain('{#if battleActive}');
    expect(content).toContain('<Swords');
    expect(content).not.toContain('{#if !battleActive}');
  });

  test('hides side sidebar in battle', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain("viewMode === 'main' && !battleActive");
  });

  test('themes start run and cancel buttons', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain('stained-glass-row');
    expect(content).toContain('Start Run');
    expect(content).toContain('Cancel');
  });

  test('wires top navigation events', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain("dispatch('home')");
    expect(content).toContain("dispatch('openEditor')");
    expect(content).toContain("dispatch('back')");
  });

  test('shows reward overlay when reward choices exist', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain('RewardOverlay');
    expect(content).toContain('relic_choices');
    expect(content).toContain('card_choices');
  });
});

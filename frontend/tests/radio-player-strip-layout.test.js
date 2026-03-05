import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('RadioPlayerStrip layout and behavior wiring', () => {
  test('uses hover-driven collapse timing with left mini art state', () => {
    const stripFile = join(import.meta.dir, '../src/lib/components/RadioPlayerStrip.svelte');
    const content = readFileSync(stripFile, 'utf8');

    expect(content).toContain('const COLLAPSE_DELAY_MS = 3000;');
    expect(content).toContain('class:collapsed={!expanded}');
    expect(content).toContain('left: 0.75rem;');
    expect(content).toContain('width: calc(100vw - 1.5rem);');
    expect(content).toContain('width: 56px;');
    expect(content).toContain('transform-origin: bottom left;');
    expect(content).toContain('on:pointerenter={handlePointerEnter}');
    expect(content).toContain('on:pointerleave={handlePointerLeave}');
    expect(content).toContain('border-radius: 0;');
    expect(content).not.toContain('{#if expanded}');
  });

  test('keeps center icon-only controls and right-side channel+volume utilities', () => {
    const stripFile = join(import.meta.dir, '../src/lib/components/RadioPlayerStrip.svelte');
    const content = readFileSync(stripFile, 'utf8');

    expect(content).toContain('<SkipBack');
    expect(content).toContain('<Play');
    expect(content).toContain('<Pause');
    expect(content).toContain('<SkipForward');
    expect(content).toContain('<SignalHigh');
    expect(content).toContain('class=\"selectors\"');
    expect(content).toContain('value={runtime.channel} on:change');
    expect(content).toContain('type=\"range\"');
    expect(content).not.toContain('qualityLabel');
    expect(content).not.toContain('<AudioLines');
  });

  test('includes dynamic art palette extraction and dim overlay layers', () => {
    const stripFile = join(import.meta.dir, '../src/lib/components/RadioPlayerStrip.svelte');
    const content = readFileSync(stripFile, 'utf8');

    expect(content).toContain('const paletteCache = new Map();');
    expect(content).toContain('async function extractPalette(url)');
    expect(content).toContain('rgba(var(--radio-primary)');
    expect(content).toContain('rgba(var(--radio-dim)');
    expect(content).toContain('Midori AI Radio:');
  });
});

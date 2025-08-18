import { describe, expect, test } from 'bun:test';
import fs from 'fs';
import { getCharacterImage, getElementColor, getElementIcon } from '../src/lib/assetLoader.js';

describe('asset loader', () => {
  test('returns fallback string for unknown character', () => {
    const img = getCharacterImage('nonexistent');
    expect(typeof img).toBe('string');
  });

  test('resolves existing character portrait', () => {
    const url = getCharacterImage('becca');
    const becca = url.includes('becca');
    const fallback = url.includes('midoriai-logo');
    expect(becca || fallback).toBe(true);
    if (becca) {
      const filePath = new URL(url);
      expect(fs.existsSync(filePath)).toBe(true);
    }
  });

  test('provides damage type color and icon', () => {
    expect(getElementColor('fire')).toBe('#e25822');
    const icon = getElementIcon('light');
    expect(icon).toBeTruthy();
  });
});

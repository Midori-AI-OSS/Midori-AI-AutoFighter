import { describe, expect, test } from 'bun:test';
import { getCharacterImage, getElementColor, getElementIcon } from '../src/lib/assetLoader.js';

describe('asset loader', () => {
  test('returns string or null for unknown character', () => {
    const img = getCharacterImage('nonexistent');
    expect(img === null || typeof img === 'string').toBe(true);
  });

  test('provides damage type color and icon', () => {
    expect(getElementColor('fire')).toBe('#e25822');
    const icon = getElementIcon('light');
    expect(icon).toBeTruthy();
  });
});

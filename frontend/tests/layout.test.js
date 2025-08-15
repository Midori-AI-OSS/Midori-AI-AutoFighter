import { describe, expect, test } from 'bun:test';
import { layoutForWidth } from '../src/lib/layout.js';

describe('layoutForWidth', () => {
  test('detects desktop', () => {
    expect(layoutForWidth(1200)).toBe('desktop');
  });

  test('detects tablet', () => {
    expect(layoutForWidth(800)).toBe('tablet');
  });

  test('detects phone', () => {
    expect(layoutForWidth(400)).toBe('phone');
  });
});

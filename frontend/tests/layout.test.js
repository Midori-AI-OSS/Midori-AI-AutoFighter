import { describe, expect, test } from 'bun:test';
import { layoutForWidth, panelsForWidth } from '../src/lib/layout.js';

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

describe('panelsForWidth', () => {
  test('desktop shows party and target panels', () => {
    expect(panelsForWidth(1200)).toEqual(['party', 'target']);
  });

  test('tablet shows party picker only', () => {
    expect(panelsForWidth(800)).toEqual(['party']);
  });

  test('phone shows no side panels', () => {
    expect(panelsForWidth(400)).toEqual([]);
  });
});

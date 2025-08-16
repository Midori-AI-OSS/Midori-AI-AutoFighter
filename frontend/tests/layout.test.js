import { describe, expect, test } from 'bun:test';
import { layoutForWidth } from '../src/lib/layout.js';
import { FEEDBACK_URL } from '../src/lib/constants.js';

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

  test('feedback URL points to repository issues', () => {
    expect(FEEDBACK_URL).toBe(
      'https://github.com/Midori-AI/Midori-AI-AutoFighter/issues/new?title=Feedback&body=...'
    );
  });
});

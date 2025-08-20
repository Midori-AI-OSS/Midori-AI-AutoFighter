import { describe, expect, test } from 'bun:test';
import { getRewardArt, randomCardArt } from '../src/lib/rewardLoader.js';

describe('reward loader card art', () => {
  test('random card art always resolves', () => {
    for (let i = 0; i < 5; i++) {
      const art = randomCardArt();
      expect(typeof art).toBe('string');
      expect(art.length).toBeGreaterThan(0);
    }
  });

  test('fallback card art is used for unknown ids', () => {
    const art = getRewardArt('card', 'nonexistent-card');
    expect(typeof art).toBe('string');
    expect(art.length).toBeGreaterThan(0);
    expect(art).toContain('bg_attack_default_gray2.png');
  });
});

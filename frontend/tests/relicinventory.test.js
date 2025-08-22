import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('RelicInventory', () => {
  test('shows tooltip with description', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/RelicInventory.svelte'), 'utf8');
    expect(content).toContain('title={relic.about}');
    expect(content).toContain('relic.stacks');
  });
});

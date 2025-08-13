import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('MapDisplay component', () => {
  test('uses lucide icons and data test id', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/MapDisplay.svelte'), 'utf8');
    expect(content).toContain('lucide-svelte');
    expect(content).toContain('data-testid="map-display"');
  });
});

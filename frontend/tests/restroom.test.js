import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('RestRoom component', () => {
  test('offers craft option', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/RestRoom.svelte'), 'utf8');
    expect(content).toContain('Craft');
  });
});

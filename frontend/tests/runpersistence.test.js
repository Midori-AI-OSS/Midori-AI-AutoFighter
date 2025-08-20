import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Run persistence', () => {
  const content = readFileSync(join(import.meta.dir, '../src/routes/+page.svelte'), 'utf8');

  test('restores saved run on load', () => {
    expect(content).toContain("localStorage.getItem('runState')");
    expect(content).toContain('getMap');
  });

  test('saves run state after room entry', () => {
    expect(content).toContain("localStorage.setItem('runState'");
  });
});

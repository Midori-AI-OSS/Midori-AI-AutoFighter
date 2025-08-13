import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('PartyPicker component', () => {
  test('contains party picker markup', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/PartyPicker.svelte'), 'utf8');
    expect(content).toContain('data-testid="party-picker"');
  });

  test('includes add/remove control', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/PartyPicker.svelte'), 'utf8');
    expect(content).toContain('Add to party');
  });
});


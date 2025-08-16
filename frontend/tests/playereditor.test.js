import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('PlayerEditor component', () => {
  test('contains editor fields', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/PlayerEditor.svelte'), 'utf8');
    expect(content).toContain('data-testid="player-editor"');
    expect(content).toContain('label for="pronouns"');
    expect(content).toContain('label for="damage"');
    expect(content).toContain('damageType');
    expect(content).toContain('hp: +hp');
  });
});

import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Framerate persistence', () => {
  test('GameViewport loads saved framerate', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/GameViewport.svelte'), 'utf8');
    expect(content).toContain('if (saved.framerate !== undefined) framerate = Number(saved.framerate);');
  });
});

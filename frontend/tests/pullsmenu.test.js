import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('PullsMenu component', () => {
  test('renders pity and buttons', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/PullsMenu.svelte'), 'utf8');
    expect(content).toContain('data-testid="pulls-menu"');
    expect(content).toContain('Pull 1');
    expect(content).toContain('Pull 10');
    expect(content).toContain('(items.ticket || 0) < 1');
  });
});

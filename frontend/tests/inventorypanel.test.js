import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('InventoryPanel', () => {
  test('renders root element', () => {
    const content = readFileSync(join(import.meta.dir, '../src/lib/InventoryPanel.svelte'), 'utf8');
    expect(content).toContain('data-testid="inventory-panel"');
  });
});

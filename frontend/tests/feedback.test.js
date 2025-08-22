import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Feedback button', () => {
  test('page provides a feedback link', () => {
    const page = readFileSync(join(import.meta.dir, '../src/routes/+page.svelte'), 'utf8');
    const menu = readFileSync(join(import.meta.dir, '../src/lib/MainMenu.svelte'), 'utf8');
    expect(menu).toContain('MessageSquare');
    expect(menu).toContain("label: 'Feedback'");
    expect(page).toContain('FEEDBACK_URL');
    expect(page).toContain("window.open(FEEDBACK_URL, '_blank', 'noopener')");
  });
});

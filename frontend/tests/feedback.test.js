import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Feedback button', () => {
  test('page provides a feedback link', () => {
    const content = readFileSync(join(import.meta.dir, '../src/routes/+page.svelte'), 'utf8');
    expect(content).toContain('MessageSquare');
    expect(content).toContain("label: 'Feedback'");
    expect(content).toContain('FEEDBACK_URL');
    expect(content).toContain("window.open(FEEDBACK_URL, '_blank', 'noopener')");
  });
});

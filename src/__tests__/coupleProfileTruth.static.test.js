import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/coupleApi.js'), 'utf8');

describe('couple profile real-data truth guards', () => {
  test('discloses missing partner profile instead of inventing one', () => {
    expect(source).toContain('partnerProfileAvailable: Boolean(partnerProfile)');
    expect(source).toContain('partner: fromDatabase(partnerProfile)');
  });

  test('keeps backend relationship status nullable when absent', () => {
    expect(source).toContain('status: couple.status || null');
  });

  test('validates dates and requires backend update confirmation', () => {
    expect(source).toContain('if (!isValidDate(startedAt))');
    expect(source).toContain("return createApiError('Couple not updated'");
  });
});

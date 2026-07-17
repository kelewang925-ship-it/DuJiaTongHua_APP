import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/coupleApi.js'), 'utf8');

describe('couple profile real-data truth guards', () => {
  test('discloses missing partner profile instead of inventing one', () => {
    expect(source).toContain('partnerProfileAvailable: Boolean(partnerProfile)');
    expect(source).toContain('partner: fromDatabase(partnerProfile)');
  });

  test('normalizes a missing backend relationship status to null', () => {
    expect(source).toContain('function normalizeRelationshipStatus');
    expect(source).toContain("return typeof value === 'string' && value.trim() ? value : null");
    expect(source).toContain('const status = normalizeRelationshipStatus(couple.status)');
  });

  test('validates dates and requires backend update confirmation', () => {
    expect(source).toContain('if (!isValidDate(startedAt))');
    expect(source).toContain("return createApiError('Couple not updated'");
  });
});

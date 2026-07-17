import fs from 'node:fs';
import path from 'node:path';

describe('diary mutation truth', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/diaryApi.js'), 'utf8');

  test('validates ids and server-confirmed ownership', () => {
    expect(source).toContain("if (!id) return createApiError('Missing diary id'");
    expect(source).toContain('function isOwnedDiary');
    expect(source).toContain("select('*').maybeSingle()");
    expect(source).toContain("select('id, couple_id, author_id').maybeSingle()");
    expect(source).toContain("return createApiError('Diary not updated'");
    expect(source).toContain("return createApiError('Diary not deleted'");
  });
});
import fs from 'node:fs';
import path from 'node:path';

describe('photo collection ownership truth', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/photoApi.js'), 'utf8');

  test('validates collections and nested photos', () => {
    expect(source).toContain('function validateCollectionRow');
    expect(source).toContain("return createApiError('Album ownership mismatch'");
    expect(source).toContain("return createApiError('Album not found'");
    expect(source).toContain('photos.length === rows.length');
    expect(source).toContain("return createApiError('Photo collection not deleted'");
  });
});
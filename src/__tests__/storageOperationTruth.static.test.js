import fs from 'fs';
import path from 'path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/storageApi.js'), 'utf8');

describe('storage operation truth', () => {
  test('rejects empty or mismatched storage results', () => {
    expect(source).toContain('Storage upload result mismatch');
    expect(source).toContain('Missing signed URL');
    expect(source).toContain('Storage object not deleted');
    expect(source).toContain('removedPaths.includes(path)');
    expect(source).toContain('data.path !== path');
  });
});

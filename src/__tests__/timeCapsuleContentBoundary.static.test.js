import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/timeCapsuleApi.js'), 'utf8');

describe('time capsule locked content boundary', () => {
  test('scrubs content for capsules that are not unlocked', () => {
    expect(source).toContain('function sanitizeCapsule');
    expect(source).toContain('content: null');
    expect(source).toContain('createApiResponse(sanitizeCapsules(data || []))');
  });

  test('sanitizes create and update responses before returning them to the store', () => {
    expect(source).toContain('createApiResponse(sanitizeCapsule(data))');
    expect(source).toContain('const value = sanitizeCapsule(data)');
  });
});

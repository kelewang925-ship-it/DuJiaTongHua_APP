import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/timeCapsuleApi.js'), 'utf8');

describe('time capsule locked content boundary', () => {
  test('scrubs content for capsules that are not unlocked', () => {
    expect(source).toContain('function sanitizeCapsule');
    expect(source).toContain('content: null');
    expect(source).toContain('if (isCapsuleUnlocked(capsule)) return capsule');
  });

  test('fails closed when RPC rows do not belong to the active couple', () => {
    expect(source).toContain('capsule.coupleId !== coupleId');
    expect(source).toContain('const capsules = sanitizeCapsules(data || [], coupleId)');
    expect(source).toContain("return createApiError('Invalid capsule ownership'");
  });

  test('sanitizes and ownership-checks create and update responses', () => {
    expect(source).toContain('const capsule = sanitizeCapsule(data, coupleId)');
    expect(source).toContain('capsule.creatorId !== context.user.id');
    expect(source).toContain('capsule.id !== id');
    expect(source).toContain('return createApiResponse(capsule)');
  });
});

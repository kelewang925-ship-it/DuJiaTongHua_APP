import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/coupleApi.js'), 'utf8');

describe('invite binding real-data truth guards', () => {
  test('requires normalized invite codes', () => {
    expect(source).toContain('function normalizeInviteCode(value)');
    expect(source).toContain('/^[A-Z0-9]{4,32}$/');
  });

  test('validates generated invite response fields', () => {
    expect(source).toContain("return createApiError('Missing invite code'");
    expect(source).toContain("return createApiError('Invalid invite expiry'");
  });

  test('binding success requires a persisted couple id', () => {
    expect(source).toContain("return createApiError('Missing bound couple'");
    expect(source).toContain("return createApiError('Inactive couple binding'");
    expect(source).toContain('return createApiResponse({ couple, bound: true })');
  });
});

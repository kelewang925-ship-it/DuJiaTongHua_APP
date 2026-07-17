import fs from 'fs';
import path from 'path';

test('invite creation requires a future expiry', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/coupleApi.js'), 'utf8');
  expect(source).toContain('function normalizeFutureTimestamp');
  expect(source).toContain('timestamp > Date.now()');
  expect(source).toContain("createApiError('Invalid invite expiry'");
  expect(source).toContain('expiresIn: Math.max(1');
});

import fs from 'node:fs';
import path from 'node:path';

const read = (relativePath) => fs.readFileSync(path.join(process.cwd(), relativePath), 'utf8');
const home = read('app/(tabs)/index.js');
const bindConfirm = read('app/account/bind-confirm.js');

 describe('home Real data shape guards', () => {
  test('does not dereference Mock-only fields from the Store couple value', () => {
    expect(home).not.toMatch(/\bcouple\.loveDays\b/);
    expect(home).not.toMatch(/\bcouple\.statusText\b/);
    expect(home).not.toMatch(/\bcouple\.spaceName\b/);
    expect(home).toContain('deriveHomeRelationshipView(coupleState, { isReal })');
  });

  test('renders bootstrap request state with retry and a binding entry for unbound users', () => {
    expect(home).toContain('FairyRequestState');
    expect(home).toContain('loading={loading}');
    expect(home).toContain('error={loadError}');
    expect(home).toContain('onRetry={refreshCoreData}');
    expect(home).toContain('尚未完成情侣绑定');
    expect(home).toContain("router.push('/account/invite')");
  });

  test('does not fall back to Mock relationship copy in Real mode', () => {
    expect(home).toContain("relationship.spaceName");
    expect(home).toContain("relationship.loveDays == null");
    expect(home).toContain('恋爱起始日未提供');
    expect(home).not.toMatch(/isReal\s*\?[^\n]*我们的小小宇宙/);
    expect(home).not.toMatch(/isReal\s*\?[^\n]*今天也被好好爱着/);
  });
});

describe('binding duplicate request guard', () => {
  test('uses a synchronous request lock in addition to button submitting state', () => {
    expect(bindConfirm).toContain('const submissionLock = useRef(false)');
    expect(bindConfirm).toContain('if (!validInviteCode || submissionLock.current) return');
    expect(bindConfirm).toContain('submissionLock.current = true');
    expect(bindConfirm).toMatch(/submissionLock\.current = false;[\s\S]*?setSubmitting\(false\)/);
    expect(bindConfirm).toContain('disabled={submitting}');
  });
});

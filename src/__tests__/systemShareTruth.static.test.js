import fs from 'node:fs';
import path from 'node:path';

describe('system share truth static guard', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'app/share-preview.js'), 'utf8');

  test('dismissed shares are not reported as success', () => {
    expect(source).toContain('result?.action === Share.dismissedAction');
    expect(source).toContain('已取消分享，没有内容被发送。');
    expect(source).toContain('result?.action !== Share.sharedAction');
  });

  test('system share follows capability and in-flight state', () => {
    expect(source).toContain("const canSystemShare = hasCapability('systemShare')");
    expect(source).toContain('disabled={!canSystemShare || sharing}');
    expect(source).toContain('finally');
    expect(source).toContain('setSharing(false)');
  });
});

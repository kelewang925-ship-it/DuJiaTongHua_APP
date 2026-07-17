import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'app/drafts.js'), 'utf8');

describe('draft truth guards', () => {
  test('real mode identifies device-local drafts', () => {
    expect(source).toContain("这里仅展示保存在当前设备的草稿");
    expect(source).toContain("不会冒充服务器删除");
  });

  test('real mode does not locally remove AI creations', () => {
    expect(source).toContain("else if (!isReal && item.creationId) removeCreation(item.creationId)");
  });

  test('missing timestamps are disclosed', () => {
    expect(source).toContain("未提供编辑时间");
    expect(source).not.toContain("return '最近'");
  });
});
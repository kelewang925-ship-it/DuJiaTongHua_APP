import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(process.cwd(), 'app/data/backup.js'), 'utf8');

describe('backup page real-data guards', () => {
  test('does not ship fixed backup history', () => {
    expect(source).not.toContain('backup-today');
    expect(source).not.toContain('今天 20:18');
    expect(source).not.toContain('昨天 22:06');
  });

  test('does not estimate or fabricate cloud storage usage', () => {
    expect(source).not.toContain('usedStorage');
    expect(source).not.toContain('storagePercent');
    expect(source).not.toContain('GB / 5 GB');
  });

  test('does not simulate backup completion with timers', () => {
    expect(source).not.toContain('setTimeout');
    expect(source).not.toContain('所有故事都已安心收好');
    expect(source).not.toContain('已模拟恢复最近一次备份');
  });

  test('keeps destructive and remote actions disabled', () => {
    expect(source).toContain('<FairyButton title="暂未开放" disabled');
    expect(source).toContain('不会上传、覆盖或恢复任何本机数据');
  });
});

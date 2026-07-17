import fs from 'node:fs';
import path from 'node:path';

describe('store server truth', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/store/useFairyStore.js'), 'utf8');

  test('preserves confirmed writes and scopes optimistic rollback', () => {
    expect(source).toContain('serverWriteConfirmed: true');
    expect(source).toContain('refreshFailed: true');
    expect(source).toContain('const previousItem = get().timeCapsules.find');
    expect(source).toContain('item.id === id && item.readAt === optimisticReadAt');
    expect(source).toContain('Promise.allSettled');
    expect(source).toContain("setRequestState('realtime'");
  });
});
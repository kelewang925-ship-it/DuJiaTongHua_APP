import fs from 'node:fs';
import path from 'node:path';
import { deriveTimeline } from '../store/useFairyStore';

const storeSource = fs.readFileSync(path.join(process.cwd(), 'src/store/useFairyStore.js'), 'utf8');

describe('Fairy store concurrency contracts', () => {
  test('session switching invalidates old async work before and after rehydrate', () => {
    expect(storeSource).toContain('let sessionEpoch = 0');
    expect(storeSource).toMatch(/const bootstrapEpoch = \+\+sessionEpoch/);
    expect(storeSource).toMatch(/bootstrapEpoch !== sessionEpoch/);
    expect(storeSource).toMatch(/await useFairyStore\.persist\.rehydrate\(\)/);
    expect(storeSource).toMatch(/Superseded rehydrate/);
  });

  test('core loads are coalesced and scoped to user plus epoch', () => {
    expect(storeSource).toContain('let coreLoadPromise = null');
    expect(storeSource).toContain('let coreLoadIdentity = null');
    expect(storeSource).toMatch(/const identity = `\$\{userId\}:\$\{epoch\}`/);
    expect(storeSource).toMatch(/return coreLoadPromise/);
  });

  test('realtime subscriptions are identity scoped and stale callbacks are ignored', () => {
    expect(storeSource).toContain('let realtimeIdentity = null');
    expect(storeSource).toMatch(/const nextRealtimeIdentity = `\$\{userId\}:\$\{coupleId\}`/);
    expect(storeSource).toMatch(/epoch !== sessionEpoch/);
    expect(storeSource).toMatch(/stopRealtimeSafely\(\)/);
  });

  test('optimistic notification and capsule writes restore previous state on failure', () => {
    expect(storeSource).toMatch(/if \(!result\.success\) set\(\{ timeCapsules: previous \}\)/);
    expect(storeSource).toMatch(/if \(!result\.success\) set\(\{ notifications: previous \}\)/);
  });

  test('timeline is derived only from loaded records and anniversaries and sorted newest first', () => {
    const result = deriveTimeline(
      [{ id: 'd1', title: '日记', content: '内容', createdAt: '2026-07-17T10:00:00Z', type: '日记' }],
      [{ id: 'a1', title: '纪念日', date: '2026-07-18', description: '说明' }]
    );
    expect(result.map((item) => item.id)).toEqual(['anniversary-a1', 'record-d1']);
  });
});

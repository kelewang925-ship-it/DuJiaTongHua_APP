import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(__dirname, '../..');
const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8');

describe('Phase 2 Store concurrency guards', () => {
  const storeSource = read('src/store/useFairyStore.js');

  test('guards bootstrap, rehydrate and core loads with a session epoch', () => {
    expect(storeSource).toMatch(/sessionEpoch/);
    expect(storeSource).toMatch(/const bootstrapEpoch = \+\+sessionEpoch/);
    expect(storeSource).toMatch(/bootstrapEpoch !== sessionEpoch/);
    expect(storeSource).toMatch(/epoch !== sessionEpoch/);
  });

  test('deduplicates core loading and merges realtime refresh work', () => {
    expect(storeSource).toMatch(/coreLoadPromise/);
    expect(storeSource).toMatch(/coreLoadIdentity/);
    expect(storeSource).toMatch(/realtimeIdentity/);
    expect(storeSource).toMatch(/refreshTimer/);
    expect(storeSource).toMatch(/loadCoreData\(\{ force: true \}\)/);
  });

  test('stops realtime on reset and blocks Real mode mock writes', () => {
    expect(storeSource).toMatch(/stopRealtimeSafely/);
    expect(storeSource).toMatch(/resetForSession/);
    expect(storeSource).toMatch(/Real 模式不能使用本地模拟写入/);
    expect(storeSource).toMatch(/if \(IS_REAL_MODE\) return null/);
    expect(storeSource).toMatch(/if \(IS_REAL_MODE\) return false/);
  });

  test('contains rollback paths for optimistic notification and capsule changes', () => {
    expect(storeSource).toMatch(/setTimeCapsuleReminderReal/);
    expect(storeSource).toMatch(/if \(!result\.success\) set\(\{ timeCapsules: previous \}\)/);
    expect(storeSource).toMatch(/if \(!result\.success\) set\(\{ notifications: previous \}\)/);
    expect(storeSource).toMatch(/markNotificationRead/);
    expect(storeSource).toMatch(/markAllNotificationsRead/);
  });
});

describe('upload compensation guards', () => {
  const diarySource = read('src/api/diaryApi.js');
  const photoSource = read('src/api/photoApi.js');

  test('diary writes clean uploaded attachments when database writes fail', () => {
    expect(diarySource).toMatch(/cleanupAttachments/);
    expect(diarySource).toMatch(/cleanupRequired/);
    expect(diarySource).toMatch(/已回滚日记/);
  });

  test('photo collection writes clean files and rollback the collection', () => {
    expect(photoSource).toMatch(/cleanupFiles/);
    expect(photoSource).toMatch(/cleanupRequired/);
    expect(photoSource).toMatch(/已回滚照片集/);
  });
});

describe('Supabase migration static security guards', () => {
  const migrations = [
    'supabase/migrations/202607170002_initial_rls.sql',
    'supabase/migrations/202607170003_real_data_core.sql',
    'supabase/migrations/202607170004_security_hardening.sql',
    'supabase/migrations/202607170005_static_security_completion.sql',
  ].map(read).join('\n');

  test('SECURITY DEFINER functions set an explicit search_path', () => {
    const functionBlocks = migrations.split(/create or replace function/i).slice(1);
    const securityDefinerBlocks = functionBlocks.filter((block) => /security definer/i.test(block));
    expect(securityDefinerBlocks.length).toBeGreaterThan(0);
    securityDefinerBlocks.forEach((block) => expect(block).toMatch(/set search_path\s*=\s*public/i));
  });

  test('prevents client notification spoofing and direct couple membership writes', () => {
    expect(migrations).toMatch(/revoke insert, delete on public\.notifications from authenticated/i);
    expect(migrations).toMatch(/revoke insert, update, delete on public\.couples from authenticated/i);
  });

  test('protects locked capsule bodies behind RPCs', () => {
    expect(migrations).toMatch(/revoke select, update, delete on public\.time_capsules from authenticated/i);
    expect(migrations).toMatch(/get_time_capsules/);
  });

  test('requires exact couple, user and UUID Storage path segments', () => {
    expect(migrations).toMatch(/array_length\(storage\.foldername\(name\), 1\) = 3/i);
    expect(migrations).toMatch(/try_uuid\(\(storage\.foldername\(name\)\)\[3\]\) is not null/i);
  });
});

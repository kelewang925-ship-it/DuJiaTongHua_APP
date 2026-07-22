import fs from 'node:fs';
import path from 'node:path';

const read = (file) => fs.readFileSync(path.join(process.cwd(), file), 'utf8');
const capsuleApi = read('src/api/timeCapsuleApi.js');
const commentApi = read('src/api/commentApi.js');
const notificationApi = read('src/api/notificationApi.js');
const capsulePage = read('app/time-capsule/settings.js');

describe('business data safety contracts', () => {
  test('time capsules are read and mutated through controlled RPCs', () => {
    expect(capsuleApi).toMatch(/rpc\('get_time_capsules'\)/);
    expect(capsuleApi).toMatch(/rpc\('create_time_capsule'/);
    expect(capsuleApi).not.toMatch(/from\('time_capsules'\)\.insert/);
    expect(capsuleApi).toMatch(/rpc\('update_time_capsule'/);
    expect(capsuleApi).toMatch(/rpc\('delete_time_capsule'/);
    expect(capsuleApi).toMatch(/rpc\('set_time_capsule_reminder'/);
  });

  test('locked capsule page never renders stored content from list rows', () => {
    expect(capsulePage).toContain('正文已封存 · 到期前不可查看');
    expect(capsulePage).not.toMatch(/capsule\.content\s*\}/);
  });

  test('comment reads and creates are scoped to the active couple and author', () => {
    expect(commentApi).toMatch(/eq\('couple_id', coupleId\)/);
    expect(commentApi).toMatch(/couple_id: coupleId/);
    expect(commentApi).toMatch(/author_id: context\.user\.id/);
    expect(commentApi).toMatch(/eq\('author_id', context\.user\.id\)/);
  });

  test('notifications can only be read or marked for the current user', () => {
    expect(notificationApi).toMatch(/eq\('user_id', context\.user\.id\)/);
    expect(notificationApi).toMatch(/eq\('id', id\)[\s\S]*?eq\('user_id', context\.user\.id\)/);
    expect(notificationApi).not.toMatch(/\.insert\(/);
  });
});

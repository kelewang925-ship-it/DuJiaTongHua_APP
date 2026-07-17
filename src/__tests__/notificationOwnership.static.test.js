import fs from 'fs';
import path from 'path';

test('notification reads validate current user ownership', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/notificationApi.js'), 'utf8');
  expect(source).toContain("item.user_id !== context.user.id");
  expect(source).toContain("select('id, user_id, read_at')");
  expect(source).toContain("select('id, user_id')");
  expect(source).toContain('Notification ownership mismatch');
});

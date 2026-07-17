const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.join(__dirname, '../api/notificationApi.js'), 'utf8');

describe('notification read server truth', () => {
  test('single read requires an id and verifies the returned row belongs to the user', () => {
    expect(source).toContain("if (!id) return createApiError('Missing notification id'");
    expect(source).toMatch(/\.select\(['"]id, user_id, read_at['"]\)/);
    expect(source).toContain('.maybeSingle()');
    expect(source).toContain('data.user_id !== context.user.id');
    expect(source).toContain("return createApiError('Notification not updated'");
  });

  test('mark all returns only rows confirmed by the server for the current user', () => {
    expect(source).toContain(".is('read_at', null)");
    expect(source).toMatch(/\.select\(['"]id, user_id['"]\)/);
    expect(source).toContain('item.user_id !== context.user.id');
    expect(source).toContain('updatedIds: rows.map((item) => item.id)');
  });
});

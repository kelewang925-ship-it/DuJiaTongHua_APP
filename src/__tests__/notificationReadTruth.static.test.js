const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.join(__dirname, '../api/notificationApi.js'), 'utf8');

describe('notification read server truth', () => {
  test('single read requires an id and verifies the updated row', () => {
    expect(source).toContain("if (!id) return createApiError('Missing notification id'");
    expect(source).toContain(".select('id, read_at')");
    expect(source).toContain('.maybeSingle()');
    expect(source).toContain("if (!data?.id) return createApiError('Notification not updated'");
  });

  test('mark all returns the rows actually updated by the server', () => {
    expect(source).toContain(".is('read_at', null)");
    expect(source).toContain(".select('id')");
    expect(source).toContain('updatedIds: (data || []).map');
  });
});

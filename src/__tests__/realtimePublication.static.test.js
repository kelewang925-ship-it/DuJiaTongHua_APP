const fs = require('fs');
const path = require('path');

const read = (file) => fs.readFileSync(path.resolve(__dirname, '..', '..', file), 'utf8');

describe('Realtime publication migration', () => {
  test('publishes every application table that the client subscribes to', () => {
    const client = read('src/api/realtimeApi.js');
    const migration = read('supabase/migrations/202607180008_enable_realtime_publication.sql');
    const expectedTables = [
      'couples', 'diaries', 'diary_attachments', 'photo_collections', 'photos',
      'anniversaries', 'custom_tags', 'time_capsules', 'comments', 'notifications',
    ];

    expectedTables.forEach((table) => {
      expect(client).toContain(`table: '${table}'`);
      expect(migration).toContain(`'${table}'`);
    });
    expect(migration).toContain('pg_publication_tables');
    expect(migration).toContain('alter publication supabase_realtime add table public.%I');
  });
});

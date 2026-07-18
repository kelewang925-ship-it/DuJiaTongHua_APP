const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(
  path.resolve(__dirname, '..', '..', 'supabase', 'migrations', '202607180009_fix_storage_object_path_policies.sql'),
  'utf8',
);

describe('storage object path policy repair', () => {
  test('treats the UUID as the object filename rather than a third folder', () => {
    expect(source).toContain('array_length(storage.foldername(name), 1) = 2');
    expect(source).toContain('public.try_uuid(storage.filename(name)) is not null');
    expect(source).not.toContain('array_length(storage.foldername(name), 1) = 3');
    expect(source).not.toContain('(storage.foldername(name))[3]');
  });

  test('keeps member read, owner upload, and owner deletion boundaries', () => {
    expect(source).toContain('create policy "couple_storage_read"');
    expect(source).toContain('create policy "couple_storage_insert"');
    expect(source).toContain('create policy "couple_storage_delete"');
    expect(source).toContain('public.try_uuid((storage.foldername(name))[2]) = auth.uid()');
    expect(source).toContain('owner_id = auth.uid()::text');
  });
});

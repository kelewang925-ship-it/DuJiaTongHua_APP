import fs from 'node:fs';
import path from 'node:path';

const migrationDir = path.join(process.cwd(), 'supabase/migrations');
const migrationFiles = fs.readdirSync(migrationDir).filter((name) => name.endsWith('.sql')).sort();
const migrations = migrationFiles.map((name) => ({
  name,
  source: fs.readFileSync(path.join(migrationDir, name), 'utf8'),
}));
const combined = migrations.map((item) => item.source).join('\n');

describe('Supabase static security contracts', () => {
  test('migrations are ordered and include every Phase 2 security batch', () => {
    expect(migrationFiles).toEqual([...migrationFiles].sort());
    expect(migrationFiles).toEqual(expect.arrayContaining([
      '202607170001_initial_schema.sql',
      '202607170002_initial_rls.sql',
      '202607170003_real_data_core.sql',
      '202607170004_security_hardening.sql',
      '202607170005_static_security_completion.sql',
    ]));
  });

  test('security definer functions pin search_path and remove public execute access', () => {
    const definerBlocks = combined.match(/create or replace function[\s\S]*?\$\$;/gi) || [];
    expect(definerBlocks.length).toBeGreaterThan(0);
    for (const block of definerBlocks.filter((value) => /security definer/i.test(value))) {
      expect(block).toMatch(/set search_path\s*=\s*public/i);
    }
    expect(combined).toMatch(/revoke all on function public\.create_couple_invite\(\) from public/i);
    expect(combined).toMatch(/revoke all on function public\.bind_couple_by_invite\(text\) from public/i);
  });

  test('couple membership and status cannot be mutated directly by authenticated clients', () => {
    expect(combined).toMatch(/revoke insert, update, delete on public\.couples from authenticated/i);
    expect(combined).toMatch(/drop policy if exists "couples_insert_as_user_a"/i);
  });

  test('notifications cannot be forged by clients', () => {
    expect(combined).toMatch(/revoke insert, delete on public\.notifications from authenticated/i);
  });

  test('storage requires couple, user and UUID path segments', () => {
    expect(combined).toMatch(/array_length\(storage\.foldername\(name\), 1\) = 3/i);
    expect(combined).toMatch(/try_uuid\(\(storage\.foldername\(name\)\)\[3\]\) is not null/i);
    expect(combined).toMatch(/try_uuid\(\(storage\.foldername\(name\)\)\[2\]\) = auth\.uid\(\)/i);
  });

  test('locked time capsule content remains behind controlled RPC access', () => {
    expect(combined).toMatch(/revoke select, update, delete on public\.time_capsules from authenticated/i);
    expect(combined).toMatch(/grant execute on function public\.get_time_capsules\(\) to authenticated/i);
    expect(combined).toMatch(/create or replace function public\.create_time_capsule\(/i);
    expect(combined).toMatch(/revoke insert on public\.time_capsules from authenticated/i);
  });
});

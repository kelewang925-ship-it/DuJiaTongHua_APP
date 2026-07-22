import fs from 'node:fs';
import path from 'node:path';

const migrations = fs.readdirSync(path.join(process.cwd(), 'supabase/migrations'))
  .filter((file) => file.endsWith('.sql'))
  .sort()
  .map((file) => fs.readFileSync(path.join(process.cwd(), 'supabase/migrations', file), 'utf8'))
  .join('\n');

describe('time capsule mutation RPC contracts', () => {
  test('delete and reminder RPCs return a server-confirmed capsule row', () => {
    expect(migrations).toMatch(/create or replace function public\.delete_time_capsule\(p_id uuid\)[\s\S]*?returns public\.time_capsules/i);
    expect(migrations).toMatch(/create or replace function public\.set_time_capsule_reminder\(p_id uuid,p_enabled boolean\)[\s\S]*?returns public\.time_capsules/i);
    expect(migrations).toMatch(/returning \* into result/i);
  });

  test('mutation RPCs reject missing rows instead of reporting a false success', () => {
    expect(migrations).toMatch(/delete_time_capsule[\s\S]*?Time capsule not found/i);
    expect(migrations).toMatch(/set_time_capsule_reminder[\s\S]*?Time capsule not found/i);
  });
});

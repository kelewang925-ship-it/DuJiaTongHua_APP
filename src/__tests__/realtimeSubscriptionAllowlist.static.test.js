import fs from 'node:fs';
import path from 'node:path';

describe('realtime subscription allowlist static guard', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/realtimeApi.js'), 'utf8');

  test('does not subscribe with wildcard table', () => {
    expect(source).not.toContain("table: '*'");
    expect(source).toContain('COUPLE_REALTIME_TARGETS');
    expect(source).toContain("{ table: 'couples', filterColumn: 'id' }");
    expect(source).toContain("{ table: 'diaries', filterColumn: 'couple_id' }");
  });

  test('removes every created channel and ignores callbacks after cleanup', () => {
    expect(source).toContain('active = false');
    expect(source).toContain('channels.forEach((channel) => context.supabase.removeChannel(channel))');
  });
});

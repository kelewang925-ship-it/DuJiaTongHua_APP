const fs = require('fs');
const path = require('path');

const read = (file) => fs.readFileSync(path.resolve(__dirname, '..', '..', file), 'utf8');

describe('current couple controlled read path', () => {
  test('uses an authenticated RPC instead of a direct active-couple table query', () => {
    const client = read('src/api/client.js');
    const migration = read('supabase/migrations/202607180007_get_current_couple_rpc.sql');

    expect(client).toContain("supabase.rpc('get_current_couple')");
    expect(client).not.toContain(".from('couples')\n    .select('*')");
    expect(migration).toContain('security definer');
    expect(migration).toContain('and c.status = \'active\'');
    expect(migration).toContain('c.user_a = auth.uid() or c.user_b = auth.uid()');
    expect(migration).toContain('grant execute on function public.get_current_couple() to authenticated');
    expect(migration).toContain('revoke all on function public.get_current_couple() from public');
  });
});

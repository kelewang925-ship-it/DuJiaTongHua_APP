import fs from 'node:fs';
import path from 'node:path';

const read = (relativePath) => fs.readFileSync(path.join(process.cwd(), relativePath), 'utf8');
const migration = read('supabase/migrations/202607180006_allow_pending_invite_holder_to_bind.sql');
const securityCompletion = read('supabase/migrations/202607170005_static_security_completion.sql');
const invitePage = read('app/account/invite.js');
const coupleApi = read('src/api/coupleApi.js');

describe('pending invite holder binding rules', () => {
  test('unbound users still receive or reuse an invite automatically on page entry', () => {
    expect(invitePage).toMatch(/const loadInvite = useCallback\(async \(\) =>/);
    expect(invitePage).toMatch(/const result = await createInviteCode\(\)/);
    expect(invitePage).toMatch(/useEffect\(\(\) => \{[\s\S]*?loadInvite\(\)/);
    expect(invitePage).toMatch(/receivedInviteCode/);
    expect(invitePage).toMatch(/router\.push\(`\/account\/bind-confirm\?code=/);
    expect(securityCompletion).toMatch(/where user_a = auth\.uid\(\) and status = 'pending'[\s\S]*?for update/i);
    expect(securityCompletion).toMatch(/if result\.id is null then[\s\S]*?insert into public\.couples/i);
    expect(securityCompletion).toMatch(/else[\s\S]*?update public\.couples[\s\S]*?invite_expires_at = now\(\) \+ interval '1 hour'/i);
  });

  test('replaces only bind_couple_by_invite and preserves controlled RPC security', () => {
    expect(migration).toMatch(/create or replace function public\.bind_couple_by_invite\(p_invite_code text\)/i);
    expect(migration).not.toMatch(/create or replace function public\.create_couple_invite/i);
    expect(migration).toMatch(/security definer/i);
    expect(migration).toMatch(/set search_path = public/i);
    expect(migration).toMatch(/revoke all on function public\.bind_couple_by_invite\(text\) from public/i);
    expect(migration).toMatch(/revoke all on function public\.bind_couple_by_invite\(text\) from anon/i);
    expect(migration).toMatch(/grant execute on function public\.bind_couple_by_invite\(text\) to authenticated/i);
  });

  test('allows B to own a pending invite while binding A and revokes all B pending invites first', () => {
    expect(migration).not.toContain('Cancel or expire your existing invite before binding another');
    expect(migration).toMatch(/perform 1[\s\S]*?where user_a = current_user_id[\s\S]*?status = 'pending'[\s\S]*?for update/i);
    expect(migration).toMatch(/update public\.couples[\s\S]*?status = 'disconnected'[\s\S]*?invite_code = null[\s\S]*?invite_expires_at = null[\s\S]*?where user_a = current_user_id[\s\S]*?status = 'pending'/i);
    const revokePosition = migration.indexOf("set status = 'disconnected'");
    const activatePosition = migration.indexOf('set user_b = current_user_id');
    expect(revokePosition).toBeGreaterThan(-1);
    expect(activatePosition).toBeGreaterThan(revokePosition);
  });

  test('clears both invite codes and returns the target A relationship as active', () => {
    expect(migration).toMatch(/set user_b = current_user_id,[\s\S]*?status = 'active',[\s\S]*?invite_code = null,[\s\S]*?invite_expires_at = null/i);
    expect(migration).toMatch(/returning \* into result/i);
    expect(migration).toMatch(/return result;/i);
  });

  test('rejects self binding, invalid or expired codes, and active relationships', () => {
    expect(migration).toMatch(/normalized_code !~ '\^\[A-Z0-9\]\{4,32\}\$'/);
    expect(migration).toMatch(/target_owner_id = current_user_id/);
    expect(migration).toMatch(/raise exception 'Cannot bind your own invite code'/);
    expect(migration).toMatch(/invite_expires_at > now\(\)/);
    expect(migration).toMatch(/status = 'active'[\s\S]*?user_a = current_user_id or user_b = current_user_id/);
    expect(migration).toMatch(/raise exception 'Already bound to a couple'/);
    expect(securityCompletion).toMatch(/create or replace function public\.create_couple_invite[\s\S]*?raise exception 'Already bound to a couple'/i);
    expect(coupleApi).toMatch(/couple\.status !== 'active'/);
  });

  test('uses deterministic locks for both users and row locks to prevent double active binding', () => {
    expect(migration).toMatch(/least\(current_user_id::text, target_owner_id::text\)/);
    expect(migration).toMatch(/greatest\(current_user_id::text, target_owner_id::text\)/);
    expect(migration.match(/pg_advisory_xact_lock/g)).toHaveLength(2);
    expect(migration).toMatch(/select \* into result[\s\S]*?for update/i);
    expect(migration).toMatch(/status = 'active'[\s\S]*?user_a = target_owner_id or user_b = target_owner_id/i);
    expect(migration).toMatch(/raise exception 'Invite owner is already bound'/);
  });

  test('authenticated clients still cannot directly mutate couples membership or status', () => {
    expect(securityCompletion).toMatch(/revoke insert, update, delete on public\.couples from authenticated/i);
    expect(migration).not.toMatch(/grant (?:insert|update|delete) on public\.couples/i);
  });
});

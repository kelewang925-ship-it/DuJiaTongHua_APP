-- Allow an unbound user to accept another invite while still owning a pending invite.
-- Apply after 202607170005_static_security_completion.sql.

create or replace function public.bind_couple_by_invite(p_invite_code text)
returns public.couples
language plpgsql
security definer
set search_path = public
as $$
declare
  current_user_id uuid := auth.uid();
  normalized_code text := upper(trim(coalesce(p_invite_code, '')));
  target_owner_id uuid;
  result public.couples;
  first_lock_key text;
  second_lock_key text;
begin
  if current_user_id is null then
    raise exception 'Not authenticated';
  end if;

  if normalized_code !~ '^[A-Z0-9]{4,32}$' then
    raise exception 'Invalid or expired invite code';
  end if;

  -- Resolve the invitation owner before taking locks. The invitation is selected
  -- again with FOR UPDATE after both user-level locks are held.
  select user_a into target_owner_id
  from public.couples
  where upper(invite_code) = normalized_code
    and status = 'pending'
    and user_b is null
    and invite_expires_at > now()
  order by created_at desc
  limit 1;

  if target_owner_id is null then
    raise exception 'Invalid or expired invite code';
  end if;

  if target_owner_id = current_user_id then
    raise exception 'Cannot bind your own invite code';
  end if;

  -- Lock both users in deterministic UUID-text order. create_couple_invite uses
  -- the same advisory key for its owner, so invite creation/reuse and binding
  -- cannot race into two active relationships for either participant.
  first_lock_key := least(current_user_id::text, target_owner_id::text);
  second_lock_key := greatest(current_user_id::text, target_owner_id::text);
  perform pg_advisory_xact_lock(hashtextextended(first_lock_key, 0));
  perform pg_advisory_xact_lock(hashtextextended(second_lock_key, 0));

  if exists (
    select 1
    from public.couples
    where status = 'active'
      and (user_a = current_user_id or user_b = current_user_id)
  ) then
    raise exception 'Already bound to a couple';
  end if;

  if exists (
    select 1
    from public.couples
    where status = 'active'
      and (user_a = target_owner_id or user_b = target_owner_id)
  ) then
    raise exception 'Invite owner is already bound';
  end if;

  -- Revalidate and row-lock A's invitation after acquiring both user locks.
  select * into result
  from public.couples
  where upper(invite_code) = normalized_code
    and status = 'pending'
    and user_b is null
    and user_a = target_owner_id
    and invite_expires_at > now()
  order by created_at desc
  limit 1
  for update;

  if result.id is null then
    raise exception 'Invalid or expired invite code';
  end if;

  -- Lock and revoke every pending invitation owned by B. Clearing the code and
  -- expiry guarantees that no stale B invitation can be bound after this point.
  perform 1
  from public.couples
  where user_a = current_user_id
    and status = 'pending'
    and id <> result.id
  for update;

  update public.couples
  set status = 'disconnected',
      invite_code = null,
      invite_expires_at = null,
      updated_at = now()
  where user_a = current_user_id
    and status = 'pending'
    and id <> result.id;

  update public.couples
  set user_b = current_user_id,
      status = 'active',
      invite_code = null,
      invite_expires_at = null,
      updated_at = now()
  where id = result.id
    and status = 'pending'
    and user_b is null
    and user_a = target_owner_id
  returning * into result;

  if result.id is null then
    raise exception 'Invalid or expired invite code';
  end if;

  return result;
end;
$$;

revoke all on function public.bind_couple_by_invite(text) from public;
revoke all on function public.bind_couple_by_invite(text) from anon;
grant execute on function public.bind_couple_by_invite(text) to authenticated;

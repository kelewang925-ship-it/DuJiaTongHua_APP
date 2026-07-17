-- Phase 2 static security completion.
-- Apply after 202607170004_security_hardening.sql.

-- Trigger helpers are not client APIs.
revoke all on function public.set_updated_at() from public;
revoke all on function public.set_updated_at() from authenticated;

-- Couple creation, membership and status must only be changed through controlled RPCs.
drop policy if exists "couples_insert_as_user_a" on public.couples;
revoke insert, update, delete on public.couples from authenticated;

create or replace function public.create_couple_invite()
returns public.couples
language plpgsql
security definer
set search_path = public
as $$
declare
  result public.couples;
begin
  if auth.uid() is null then
    raise exception 'Not authenticated';
  end if;

  perform pg_advisory_xact_lock(hashtextextended(auth.uid()::text, 0));

  if exists (
    select 1 from public.couples
    where status = 'active'
      and (user_a = auth.uid() or user_b = auth.uid())
  ) then
    raise exception 'Already bound to a couple';
  end if;

  select * into result
  from public.couples
  where user_a = auth.uid() and status = 'pending'
  order by created_at desc
  limit 1
  for update;

  if result.id is null then
    insert into public.couples(user_a, invite_code, invite_expires_at, status)
    values (
      auth.uid(),
      upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 8)),
      now() + interval '1 hour',
      'pending'
    )
    returning * into result;
  else
    update public.couples
    set invite_code = upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 8)),
        invite_expires_at = now() + interval '1 hour',
        updated_at = now()
    where id = result.id
    returning * into result;
  end if;

  return result;
end;
$$;

create or replace function public.bind_couple_by_invite(p_invite_code text)
returns public.couples
language plpgsql
security definer
set search_path = public
as $$
declare
  result public.couples;
begin
  if auth.uid() is null then
    raise exception 'Not authenticated';
  end if;

  perform pg_advisory_xact_lock(hashtextextended(auth.uid()::text, 0));

  if exists (
    select 1 from public.couples
    where status = 'active'
      and (user_a = auth.uid() or user_b = auth.uid())
  ) then
    raise exception 'Already bound to a couple';
  end if;

  if exists (
    select 1 from public.couples
    where status = 'pending' and user_a = auth.uid()
  ) then
    raise exception 'Cancel or expire your existing invite before binding another';
  end if;

  update public.couples
  set user_b = auth.uid(),
      status = 'active',
      invite_code = null,
      invite_expires_at = null,
      updated_at = now()
  where upper(invite_code) = upper(trim(p_invite_code))
    and status = 'pending'
    and user_b is null
    and user_a <> auth.uid()
    and invite_expires_at > now()
  returning * into result;

  if result.id is null then
    raise exception 'Invalid or expired invite code';
  end if;

  return result;
end;
$$;

revoke all on function public.create_couple_invite() from public;
revoke all on function public.bind_couple_by_invite(text) from public;
grant execute on function public.create_couple_invite() to authenticated;
grant execute on function public.bind_couple_by_invite(text) to authenticated;

-- Real AI is not available in Phase 2. Prevent clients from creating or advancing jobs.
drop policy if exists "ai_jobs_insert_creator_active_couple" on public.ai_jobs;
drop policy if exists "ai_jobs_update_creator_active_couple" on public.ai_jobs;
revoke insert, update, delete on public.ai_jobs from authenticated;

-- Notifications are server/trigger-created. Clients only read and mark their own rows read.
revoke insert, delete on public.notifications from authenticated;

-- Storage paths must be exactly {coupleId}/{userId}/{uuid}.
drop policy if exists "couple_storage_read" on storage.objects;
create policy "couple_storage_read"
on storage.objects for select to authenticated
using (
  bucket_id in ('avatars', 'photos', 'diary-attachments')
  and array_length(storage.foldername(name), 1) = 3
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.try_uuid((storage.foldername(name))[2]) is not null
  and public.try_uuid((storage.foldername(name))[3]) is not null
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

drop policy if exists "couple_storage_insert" on storage.objects;
create policy "couple_storage_insert"
on storage.objects for insert to authenticated
with check (
  bucket_id in ('avatars', 'photos', 'diary-attachments')
  and array_length(storage.foldername(name), 1) = 3
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.try_uuid((storage.foldername(name))[2]) = auth.uid()
  and public.try_uuid((storage.foldername(name))[3]) is not null
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

drop policy if exists "couple_storage_delete" on storage.objects;
create policy "couple_storage_delete"
on storage.objects for delete to authenticated
using (
  bucket_id in ('avatars', 'photos', 'diary-attachments')
  and array_length(storage.foldername(name), 1) = 3
  and owner_id = auth.uid()::text
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.try_uuid((storage.foldername(name))[2]) = auth.uid()
  and public.try_uuid((storage.foldername(name))[3]) is not null
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

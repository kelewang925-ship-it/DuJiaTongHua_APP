-- Return server-confirmed rows from capsule mutations so the client can
-- distinguish a committed operation from a no-op. Apply after 202607220010.

drop function if exists public.delete_time_capsule(uuid);
create function public.delete_time_capsule(p_id uuid)
returns public.time_capsules
language plpgsql
security definer
set search_path = public
as $$
declare
  result public.time_capsules;
begin
  if auth.uid() is null then
    raise exception 'Not authenticated';
  end if;

  delete from public.time_capsules
  where id = p_id
    and public.is_active_couple_member(couple_id)
  returning * into result;

  if result.id is null then
    raise exception 'Time capsule not found';
  end if;

  return result;
end;
$$;

drop function if exists public.set_time_capsule_reminder(uuid,boolean);
create function public.set_time_capsule_reminder(p_id uuid,p_enabled boolean)
returns public.time_capsules
language plpgsql
security definer
set search_path = public
as $$
declare
  result public.time_capsules;
begin
  if auth.uid() is null or p_enabled is null then
    raise exception 'Invalid reminder value';
  end if;

  update public.time_capsules
  set reminder_enabled = p_enabled
  where id = p_id
    and public.is_active_couple_member(couple_id)
  returning * into result;

  if result.id is null then
    raise exception 'Time capsule not found';
  end if;

  return result;
end;
$$;

revoke all on function public.delete_time_capsule(uuid) from public;
revoke all on function public.delete_time_capsule(uuid) from anon;
grant execute on function public.delete_time_capsule(uuid) to authenticated;

revoke all on function public.set_time_capsule_reminder(uuid,boolean) from public;
revoke all on function public.set_time_capsule_reminder(uuid,boolean) from anon;
grant execute on function public.set_time_capsule_reminder(uuid,boolean) to authenticated;

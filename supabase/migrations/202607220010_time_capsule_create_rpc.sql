-- Capsule creation must use the same controlled-RPC boundary as reads and
-- the other mutations. Apply after 202607180009_fix_storage_object_path_policies.sql.

create or replace function public.create_time_capsule(
  p_couple_id uuid,
  p_title text,
  p_content text,
  p_unlock_date date,
  p_reminder_enabled boolean,
  p_content_types text[]
)
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

  if p_couple_id is null
    or not public.is_active_couple_member(p_couple_id)
    or p_title is null
    or length(trim(p_title)) = 0
    or p_content is null
    or length(trim(p_content)) = 0
    or p_unlock_date is null
    or p_reminder_enabled is null
    or p_content_types is null
    or cardinality(p_content_types) = 0 then
    raise exception 'Invalid time capsule payload';
  end if;

  insert into public.time_capsules (
    couple_id,
    creator_id,
    title,
    content,
    unlock_date,
    reminder_enabled,
    content_types
  )
  values (
    p_couple_id,
    auth.uid(),
    trim(p_title),
    trim(p_content),
    p_unlock_date,
    p_reminder_enabled,
    p_content_types
  )
  returning * into result;

  return result;
end;
$$;

revoke all on function public.create_time_capsule(uuid,text,text,date,boolean,text[]) from public;
revoke all on function public.create_time_capsule(uuid,text,text,date,boolean,text[]) from anon;
grant execute on function public.create_time_capsule(uuid,text,text,date,boolean,text[]) to authenticated;

-- All capsule mutations are controlled by SECURITY DEFINER functions. The
-- table remains inaccessible for direct client inserts, and locked content is
-- still protected by the existing SELECT revoke.
revoke insert on public.time_capsules from authenticated;

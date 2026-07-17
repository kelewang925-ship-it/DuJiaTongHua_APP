-- Phase 2 security hardening.
-- Apply after 202607170003_real_data_core.sql.

-- SECURITY DEFINER functions must never inherit the default PUBLIC execute grant.
revoke all on function public.is_active_couple_member(uuid) from public;
revoke all on function public.is_couple_member(uuid) from public;
revoke all on function public.create_couple_invite() from public;
revoke all on function public.bind_couple_by_invite(text) from public;
revoke all on function public.get_time_capsules() from public;
revoke all on function public.update_couple_started_at(date) from public;
revoke all on function public.update_time_capsule(uuid,text,text,date,boolean,text[]) from public;
revoke all on function public.delete_time_capsule(uuid) from public;
revoke all on function public.set_time_capsule_reminder(uuid,boolean) from public;
revoke all on function public.handle_new_user() from public;
revoke all on function public.notify_comment_target() from public;

grant execute on function public.is_active_couple_member(uuid) to authenticated;
grant execute on function public.is_couple_member(uuid) to authenticated;
grant execute on function public.create_couple_invite() to authenticated;
grant execute on function public.bind_couple_by_invite(text) to authenticated;
grant execute on function public.get_time_capsules() to authenticated;
grant execute on function public.update_couple_started_at(date) to authenticated;
grant execute on function public.update_time_capsule(uuid,text,text,date,boolean,text[]) to authenticated;
grant execute on function public.delete_time_capsule(uuid) to authenticated;
grant execute on function public.set_time_capsule_reminder(uuid,boolean) to authenticated;

-- Couple membership and status remain RPC-controlled. The legacy direct update
-- policy was removed in migration 003; explicitly revoke the table privilege too.
revoke update, delete on public.couples from authenticated;

-- Tags cannot spoof another creator and can only be changed by their creator
-- while that creator is still an active member of the couple.
drop policy if exists "custom_tags_member_all" on public.custom_tags;
drop policy if exists "custom_tags_select_member" on public.custom_tags;
drop policy if exists "custom_tags_insert_creator" on public.custom_tags;
drop policy if exists "custom_tags_update_creator" on public.custom_tags;
drop policy if exists "custom_tags_delete_creator" on public.custom_tags;

create policy "custom_tags_select_member"
on public.custom_tags for select to authenticated
using (public.is_active_couple_member(couple_id));

create policy "custom_tags_insert_creator"
on public.custom_tags for insert to authenticated
with check (
  created_by = auth.uid()
  and public.is_active_couple_member(couple_id)
);

create policy "custom_tags_update_creator"
on public.custom_tags for update to authenticated
using (
  created_by = auth.uid()
  and public.is_active_couple_member(couple_id)
)
with check (
  created_by = auth.uid()
  and public.is_active_couple_member(couple_id)
);

create policy "custom_tags_delete_creator"
on public.custom_tags for delete to authenticated
using (
  created_by = auth.uid()
  and public.is_active_couple_member(couple_id)
);

-- Owners lose mutation access after a couple is no longer active.
drop policy if exists "photo_collections_update_owner" on public.photo_collections;
create policy "photo_collections_update_owner"
on public.photo_collections for update to authenticated
using (
  uploader_id = auth.uid()
  and public.is_active_couple_member(couple_id)
)
with check (
  uploader_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "photo_collections_delete_owner" on public.photo_collections;
create policy "photo_collections_delete_owner"
on public.photo_collections for delete to authenticated
using (
  uploader_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "diary_attachments_delete_owner" on public.diary_attachments;
create policy "diary_attachments_delete_owner"
on public.diary_attachments for delete to authenticated
using (
  uploader_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

-- Locked capsule reads and all capsule mutations stay behind controlled RPCs.
revoke select, update, delete on public.time_capsules from authenticated;
grant insert on public.time_capsules to authenticated;

-- Reject malformed object paths without raising UUID cast errors inside RLS.
create or replace function public.try_uuid(value text)
returns uuid
language plpgsql
immutable
strict
set search_path = public
as $$
begin
  return value::uuid;
exception
  when invalid_text_representation then
    return null;
end;
$$;
revoke all on function public.try_uuid(text) from public;
grant execute on function public.try_uuid(text) to authenticated;

drop policy if exists "couple_storage_read" on storage.objects;
create policy "couple_storage_read"
on storage.objects for select to authenticated
using (
  bucket_id in ('avatars','photos','diary-attachments')
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

drop policy if exists "couple_storage_insert" on storage.objects;
create policy "couple_storage_insert"
on storage.objects for insert to authenticated
with check (
  bucket_id in ('avatars','photos','diary-attachments')
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.try_uuid((storage.foldername(name))[2]) = auth.uid()
  and coalesce((storage.foldername(name))[3], '') <> ''
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

drop policy if exists "couple_storage_delete" on storage.objects;
create policy "couple_storage_delete"
on storage.objects for delete to authenticated
using (
  bucket_id in ('avatars','photos','diary-attachments')
  and owner_id = auth.uid()::text
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.try_uuid((storage.foldername(name))[2]) = auth.uid()
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

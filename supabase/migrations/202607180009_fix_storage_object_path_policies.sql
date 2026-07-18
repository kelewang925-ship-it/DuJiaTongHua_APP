-- Storage path format is {coupleId}/{userId}/{uuid}. In storage.objects,
-- foldername(name) returns only directory segments; the UUID is filename(name).
-- Apply after 202607180008_enable_realtime_publication.sql.

drop policy if exists "couple_storage_read" on storage.objects;
create policy "couple_storage_read"
on storage.objects for select to authenticated
using (
  bucket_id in ('avatars', 'photos', 'diary-attachments')
  and array_length(storage.foldername(name), 1) = 2
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.try_uuid((storage.foldername(name))[2]) is not null
  and public.try_uuid(storage.filename(name)) is not null
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

drop policy if exists "couple_storage_insert" on storage.objects;
create policy "couple_storage_insert"
on storage.objects for insert to authenticated
with check (
  bucket_id in ('avatars', 'photos', 'diary-attachments')
  and array_length(storage.foldername(name), 1) = 2
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.try_uuid((storage.foldername(name))[2]) = auth.uid()
  and public.try_uuid(storage.filename(name)) is not null
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

drop policy if exists "couple_storage_delete" on storage.objects;
create policy "couple_storage_delete"
on storage.objects for delete to authenticated
using (
  bucket_id in ('avatars', 'photos', 'diary-attachments')
  and array_length(storage.foldername(name), 1) = 2
  and owner_id = auth.uid()::text
  and public.try_uuid((storage.foldername(name))[1]) is not null
  and public.try_uuid((storage.foldername(name))[2]) = auth.uid()
  and public.try_uuid(storage.filename(name)) is not null
  and public.is_active_couple_member(public.try_uuid((storage.foldername(name))[1]))
);

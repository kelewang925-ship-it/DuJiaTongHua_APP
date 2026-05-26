-- 《独家童话》Supabase Row Level Security policies
-- Phase 5.2: RLS for core tables.
-- Run this after supabase/schema.sql.

-- -----------------------------------------------------------------------------
-- Helper functions
-- -----------------------------------------------------------------------------

create or replace function public.is_active_couple_member(target_couple_id uuid)
returns boolean
language sql
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.couples c
    where c.id = target_couple_id
      and c.status = 'active'
      and (c.user_a = auth.uid() or c.user_b = auth.uid())
  );
$$;

create or replace function public.is_couple_member(target_couple_id uuid)
returns boolean
language sql
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.couples c
    where c.id = target_couple_id
      and (c.user_a = auth.uid() or c.user_b = auth.uid())
  );
$$;

create or replace function public.bind_couple_by_invite(p_invite_code text)
returns public.couples
language plpgsql
security definer
set search_path = public
as $$
declare
  updated_couple public.couples;
begin
  if auth.uid() is null then
    raise exception 'Not authenticated';
  end if;

  update public.couples
  set
    user_b = auth.uid(),
    status = 'active',
    updated_at = now()
  where invite_code = p_invite_code
    and status = 'pending'
    and user_b is null
    and user_a <> auth.uid()
  returning * into updated_couple;

  if updated_couple.id is null then
    raise exception 'Invalid or expired invite code';
  end if;

  return updated_couple;
end;
$$;

-- -----------------------------------------------------------------------------
-- Enable RLS
-- -----------------------------------------------------------------------------

alter table public.profiles enable row level security;
alter table public.couples enable row level security;
alter table public.diaries enable row level security;
alter table public.photos enable row level security;
alter table public.anniversaries enable row level security;
alter table public.ai_jobs enable row level security;
alter table public.comments enable row level security;
alter table public.notifications enable row level security;

-- -----------------------------------------------------------------------------
-- profiles
-- Users can only access and edit their own profile.
-- -----------------------------------------------------------------------------

drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own"
on public.profiles
for select
to authenticated
using (id = auth.uid());

drop policy if exists "profiles_insert_own" on public.profiles;
create policy "profiles_insert_own"
on public.profiles
for insert
to authenticated
with check (id = auth.uid());

drop policy if exists "profiles_update_own" on public.profiles;
create policy "profiles_update_own"
on public.profiles
for update
to authenticated
using (id = auth.uid())
with check (id = auth.uid());

-- Profiles are normally kept for account history. Delete is handled by auth cascade.

-- -----------------------------------------------------------------------------
-- couples
-- Direct access is limited to current members.
-- Pending invite binding should use public.bind_couple_by_invite(invite_code).
-- -----------------------------------------------------------------------------

drop policy if exists "couples_select_member" on public.couples;
create policy "couples_select_member"
on public.couples
for select
to authenticated
using (user_a = auth.uid() or user_b = auth.uid());

drop policy if exists "couples_insert_as_user_a" on public.couples;
create policy "couples_insert_as_user_a"
on public.couples
for insert
to authenticated
with check (user_a = auth.uid());

drop policy if exists "couples_update_member" on public.couples;
create policy "couples_update_member"
on public.couples
for update
to authenticated
using (user_a = auth.uid() or user_b = auth.uid())
with check (user_a = auth.uid() or user_b = auth.uid());

-- Do not allow client-side deletes for couple relationships in MVP.
-- Use an Edge Function/admin workflow if relationship deletion is needed.

-- -----------------------------------------------------------------------------
-- diaries
-- Active couple members can read diaries. Authors can create/update/delete own rows.
-- -----------------------------------------------------------------------------

drop policy if exists "diaries_select_active_couple" on public.diaries;
create policy "diaries_select_active_couple"
on public.diaries
for select
to authenticated
using (public.is_active_couple_member(couple_id));

drop policy if exists "diaries_insert_author_active_couple" on public.diaries;
create policy "diaries_insert_author_active_couple"
on public.diaries
for insert
to authenticated
with check (
  author_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "diaries_update_author_active_couple" on public.diaries;
create policy "diaries_update_author_active_couple"
on public.diaries
for update
to authenticated
using (
  author_id = auth.uid()
  and public.is_active_couple_member(couple_id)
)
with check (
  author_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "diaries_delete_author_active_couple" on public.diaries;
create policy "diaries_delete_author_active_couple"
on public.diaries
for delete
to authenticated
using (
  author_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

-- -----------------------------------------------------------------------------
-- photos
-- Active couple members can read photos. Uploaders can create/update/delete own rows.
-- -----------------------------------------------------------------------------

drop policy if exists "photos_select_active_couple" on public.photos;
create policy "photos_select_active_couple"
on public.photos
for select
to authenticated
using (public.is_active_couple_member(couple_id));

drop policy if exists "photos_insert_uploader_active_couple" on public.photos;
create policy "photos_insert_uploader_active_couple"
on public.photos
for insert
to authenticated
with check (
  uploader_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "photos_update_uploader_active_couple" on public.photos;
create policy "photos_update_uploader_active_couple"
on public.photos
for update
to authenticated
using (
  uploader_id = auth.uid()
  and public.is_active_couple_member(couple_id)
)
with check (
  uploader_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "photos_delete_uploader_active_couple" on public.photos;
create policy "photos_delete_uploader_active_couple"
on public.photos
for delete
to authenticated
using (
  uploader_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

-- -----------------------------------------------------------------------------
-- anniversaries
-- Both active couple members can manage shared anniversaries.
-- -----------------------------------------------------------------------------

drop policy if exists "anniversaries_select_active_couple" on public.anniversaries;
create policy "anniversaries_select_active_couple"
on public.anniversaries
for select
to authenticated
using (public.is_active_couple_member(couple_id));

drop policy if exists "anniversaries_insert_active_couple" on public.anniversaries;
create policy "anniversaries_insert_active_couple"
on public.anniversaries
for insert
to authenticated
with check (public.is_active_couple_member(couple_id));

drop policy if exists "anniversaries_update_active_couple" on public.anniversaries;
create policy "anniversaries_update_active_couple"
on public.anniversaries
for update
to authenticated
using (public.is_active_couple_member(couple_id))
with check (public.is_active_couple_member(couple_id));

drop policy if exists "anniversaries_delete_active_couple" on public.anniversaries;
create policy "anniversaries_delete_active_couple"
on public.anniversaries
for delete
to authenticated
using (public.is_active_couple_member(couple_id));

-- -----------------------------------------------------------------------------
-- ai_jobs
-- Active couple members can read AI jobs. Creators can create/update own jobs.
-- Deletion is intentionally not exposed to clients in MVP.
-- -----------------------------------------------------------------------------

drop policy if exists "ai_jobs_select_active_couple" on public.ai_jobs;
create policy "ai_jobs_select_active_couple"
on public.ai_jobs
for select
to authenticated
using (public.is_active_couple_member(couple_id));

drop policy if exists "ai_jobs_insert_creator_active_couple" on public.ai_jobs;
create policy "ai_jobs_insert_creator_active_couple"
on public.ai_jobs
for insert
to authenticated
with check (
  creator_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "ai_jobs_update_creator_active_couple" on public.ai_jobs;
create policy "ai_jobs_update_creator_active_couple"
on public.ai_jobs
for update
to authenticated
using (
  creator_id = auth.uid()
  and public.is_active_couple_member(couple_id)
)
with check (
  creator_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

-- Edge Functions using the service role can update status/progress/result_urls.

-- -----------------------------------------------------------------------------
-- comments
-- Active couple members can read comments. Authors can create/update/delete own comments.
-- -----------------------------------------------------------------------------

drop policy if exists "comments_select_active_couple" on public.comments;
create policy "comments_select_active_couple"
on public.comments
for select
to authenticated
using (public.is_active_couple_member(couple_id));

drop policy if exists "comments_insert_author_active_couple" on public.comments;
create policy "comments_insert_author_active_couple"
on public.comments
for insert
to authenticated
with check (
  author_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "comments_update_author_active_couple" on public.comments;
create policy "comments_update_author_active_couple"
on public.comments
for update
to authenticated
using (
  author_id = auth.uid()
  and public.is_active_couple_member(couple_id)
)
with check (
  author_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

drop policy if exists "comments_delete_author_active_couple" on public.comments;
create policy "comments_delete_author_active_couple"
on public.comments
for delete
to authenticated
using (
  author_id = auth.uid()
  and public.is_active_couple_member(couple_id)
);

-- -----------------------------------------------------------------------------
-- notifications
-- Users can only read/update/delete their own notifications.
-- Inserts are allowed for self-created local/system-like events in MVP; server-side
-- notification creation should later move to Edge Functions/service role.
-- -----------------------------------------------------------------------------

drop policy if exists "notifications_select_own" on public.notifications;
create policy "notifications_select_own"
on public.notifications
for select
to authenticated
using (user_id = auth.uid());

drop policy if exists "notifications_insert_own" on public.notifications;
create policy "notifications_insert_own"
on public.notifications
for insert
to authenticated
with check (user_id = auth.uid());

drop policy if exists "notifications_update_own" on public.notifications;
create policy "notifications_update_own"
on public.notifications
for update
to authenticated
using (user_id = auth.uid())
with check (user_id = auth.uid());

drop policy if exists "notifications_delete_own" on public.notifications;
create policy "notifications_delete_own"
on public.notifications
for delete
to authenticated
using (user_id = auth.uid());

-- -----------------------------------------------------------------------------
-- Grants
-- -----------------------------------------------------------------------------

grant usage on schema public to authenticated;
grant execute on function public.is_active_couple_member(uuid) to authenticated;
grant execute on function public.is_couple_member(uuid) to authenticated;
grant execute on function public.bind_couple_by_invite(text) to authenticated;

-- -----------------------------------------------------------------------------
-- Storage policy reminder
-- -----------------------------------------------------------------------------

-- Storage buckets and storage.objects policies are not defined here because the
-- buckets may be created from the Supabase dashboard or a later migration.
-- When buckets exist, add policies for:
-- - avatars
-- - photos
-- - ai-comics
-- - ai-videos
-- - exports
-- and restrict paths by couple_id/user_id or use signed URLs via Edge Functions.

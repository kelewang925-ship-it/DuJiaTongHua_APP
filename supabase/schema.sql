-- 《独家童话》Supabase database schema
-- Phase 5.1: core table structure only.
-- RLS policies are intentionally handled in Phase 5.2 via supabase/rls-policies.sql.

create extension if not exists "pgcrypto";

-- -----------------------------------------------------------------------------
-- Shared helpers
-- -----------------------------------------------------------------------------

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- -----------------------------------------------------------------------------
-- profiles
-- User profile extension for Supabase Auth.
-- -----------------------------------------------------------------------------

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  nickname text not null default '童话收藏家',
  avatar_url text,
  avatar_text text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger set_profiles_updated_at
before update on public.profiles
for each row
execute function public.set_updated_at();

-- -----------------------------------------------------------------------------
-- couples
-- Stores couple relationship and invite state.
-- -----------------------------------------------------------------------------

create table if not exists public.couples (
  id uuid primary key default gen_random_uuid(),
  user_a uuid not null references auth.users(id) on delete cascade,
  user_b uuid references auth.users(id) on delete set null,
  started_at date,
  invite_code text unique,
  status text not null default 'pending' check (status in ('pending', 'active', 'disconnected')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint couples_users_not_same check (user_b is null or user_a <> user_b)
);

create trigger set_couples_updated_at
before update on public.couples
for each row
execute function public.set_updated_at();

create index if not exists idx_couples_user_a on public.couples(user_a);
create index if not exists idx_couples_user_b on public.couples(user_b);
create index if not exists idx_couples_status on public.couples(status);
create index if not exists idx_couples_invite_code on public.couples(invite_code);

-- -----------------------------------------------------------------------------
-- diaries
-- Daily diary records.
-- -----------------------------------------------------------------------------

create table if not exists public.diaries (
  id uuid primary key default gen_random_uuid(),
  couple_id uuid not null references public.couples(id) on delete cascade,
  author_id uuid not null references auth.users(id) on delete cascade,
  title text not null default '今天的小小童话',
  content text not null default '',
  mood text,
  tags text[] not null default '{}',
  cover_photo_url text,
  is_private boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger set_diaries_updated_at
before update on public.diaries
for each row
execute function public.set_updated_at();

create index if not exists idx_diaries_couple_created_at on public.diaries(couple_id, created_at desc);
create index if not exists idx_diaries_author_created_at on public.diaries(author_id, created_at desc);
create index if not exists idx_diaries_tags on public.diaries using gin(tags);

-- -----------------------------------------------------------------------------
-- photos
-- Photo records and album items.
-- -----------------------------------------------------------------------------

create table if not exists public.photos (
  id uuid primary key default gen_random_uuid(),
  couple_id uuid not null references public.couples(id) on delete cascade,
  uploader_id uuid not null references auth.users(id) on delete cascade,
  title text not null default '新的照片',
  note text,
  file_url text not null,
  thumbnail_url text,
  taken_at timestamptz,
  tags text[] not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger set_photos_updated_at
before update on public.photos
for each row
execute function public.set_updated_at();

create index if not exists idx_photos_couple_created_at on public.photos(couple_id, created_at desc);
create index if not exists idx_photos_uploader_created_at on public.photos(uploader_id, created_at desc);
create index if not exists idx_photos_tags on public.photos using gin(tags);

-- -----------------------------------------------------------------------------
-- anniversaries
-- Important dates for a couple.
-- -----------------------------------------------------------------------------

create table if not exists public.anniversaries (
  id uuid primary key default gen_random_uuid(),
  couple_id uuid not null references public.couples(id) on delete cascade,
  title text not null,
  date date not null,
  repeat_type text not null default 'yearly' check (repeat_type in ('none', 'yearly', 'monthly')),
  description text,
  template_type text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger set_anniversaries_updated_at
before update on public.anniversaries
for each row
execute function public.set_updated_at();

create index if not exists idx_anniversaries_couple_date on public.anniversaries(couple_id, date);
create index if not exists idx_anniversaries_repeat_type on public.anniversaries(repeat_type);

-- -----------------------------------------------------------------------------
-- ai_jobs
-- AI comic/video generation tasks.
-- -----------------------------------------------------------------------------

create table if not exists public.ai_jobs (
  id uuid primary key default gen_random_uuid(),
  couple_id uuid not null references public.couples(id) on delete cascade,
  creator_id uuid not null references auth.users(id) on delete cascade,
  type text not null check (type in ('comic', 'video')),
  source_type text not null default 'text' check (source_type in ('diary', 'photo', 'text')),
  source_ids text[] not null default '{}',
  style text,
  character_profile jsonb not null default '{}'::jsonb,
  prompt text,
  status text not null default 'pending' check (status in ('pending', 'processing', 'done', 'failed')),
  progress int not null default 0 check (progress >= 0 and progress <= 100),
  result_urls text[] not null default '{}',
  error_message text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger set_ai_jobs_updated_at
before update on public.ai_jobs
for each row
execute function public.set_updated_at();

create index if not exists idx_ai_jobs_couple_created_at on public.ai_jobs(couple_id, created_at desc);
create index if not exists idx_ai_jobs_creator_created_at on public.ai_jobs(creator_id, created_at desc);
create index if not exists idx_ai_jobs_status on public.ai_jobs(status);
create index if not exists idx_ai_jobs_type on public.ai_jobs(type);
create index if not exists idx_ai_jobs_source_ids on public.ai_jobs using gin(source_ids);

-- -----------------------------------------------------------------------------
-- comments
-- Couple comments for diary/photo/AI creation targets.
-- -----------------------------------------------------------------------------

create table if not exists public.comments (
  id uuid primary key default gen_random_uuid(),
  couple_id uuid not null references public.couples(id) on delete cascade,
  target_type text not null check (target_type in ('diary', 'photo', 'ai_creation')),
  target_id uuid not null,
  author_id uuid not null references auth.users(id) on delete cascade,
  content text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger set_comments_updated_at
before update on public.comments
for each row
execute function public.set_updated_at();

create index if not exists idx_comments_couple_created_at on public.comments(couple_id, created_at desc);
create index if not exists idx_comments_target on public.comments(target_type, target_id, created_at asc);
create index if not exists idx_comments_author_created_at on public.comments(author_id, created_at desc);

-- -----------------------------------------------------------------------------
-- notifications
-- Interaction and system messages.
-- -----------------------------------------------------------------------------

create table if not exists public.notifications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  type text not null,
  title text not null,
  content text,
  target_type text,
  target_id uuid,
  read_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger set_notifications_updated_at
before update on public.notifications
for each row
execute function public.set_updated_at();

create index if not exists idx_notifications_user_created_at on public.notifications(user_id, created_at desc);
create index if not exists idx_notifications_user_read_at on public.notifications(user_id, read_at);
create index if not exists idx_notifications_target on public.notifications(target_type, target_id);

-- -----------------------------------------------------------------------------
-- Phase 5.2 reminder
-- -----------------------------------------------------------------------------

-- Next step:
-- 1. Create supabase/rls-policies.sql.
-- 2. Enable RLS for every table above.
-- 3. Restrict all couple-owned rows by active couple membership.
-- 4. Restrict profile rows by auth.uid() = profiles.id.

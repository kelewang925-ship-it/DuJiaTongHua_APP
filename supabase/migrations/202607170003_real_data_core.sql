-- Phase 2 real-data additions. Apply after the initial schema and RLS migrations.
alter table public.couples add column if not exists invite_expires_at timestamptz;

create table if not exists public.photo_collections (
  id uuid primary key default gen_random_uuid(), couple_id uuid not null references public.couples(id) on delete cascade,
  uploader_id uuid not null references auth.users(id) on delete cascade, title text not null default '新的照片绘本',
  note text, tags text[] not null default '{}', created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create trigger set_photo_collections_updated_at before update on public.photo_collections for each row execute function public.set_updated_at();
alter table public.photos add column if not exists collection_id uuid references public.photo_collections(id) on delete cascade;
alter table public.photos add column if not exists storage_path text;

create table if not exists public.diary_attachments (
  id uuid primary key default gen_random_uuid(), diary_id uuid not null references public.diaries(id) on delete cascade,
  couple_id uuid not null references public.couples(id) on delete cascade, uploader_id uuid not null references auth.users(id) on delete cascade,
  storage_path text not null, content_type text not null default 'image/jpeg', created_at timestamptz not null default now()
);
create table if not exists public.custom_tags (
  id uuid primary key default gen_random_uuid(), couple_id uuid not null references public.couples(id) on delete cascade,
  created_by uuid not null references auth.users(id) on delete cascade, name text not null, category text not null default '心情',
  icon text not null default 'pricetag-outline', created_at timestamptz not null default now(), updated_at timestamptz not null default now(),
  unique(couple_id, category, name)
);
create trigger set_custom_tags_updated_at before update on public.custom_tags for each row execute function public.set_updated_at();
create table if not exists public.time_capsules (
  id uuid primary key default gen_random_uuid(), couple_id uuid not null references public.couples(id) on delete cascade,
  creator_id uuid not null references auth.users(id) on delete cascade, title text not null, content text not null, unlock_date date not null,
  reminder_enabled boolean not null default true, content_types text[] not null default '{}', created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create trigger set_time_capsules_updated_at before update on public.time_capsules for each row execute function public.set_updated_at();

create or replace function public.handle_new_user() returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles(id, nickname, avatar_text)
  values(new.id, coalesce(new.raw_user_meta_data->>'nickname', new.email, '童话收藏家'), left(coalesce(new.raw_user_meta_data->>'nickname', '童'), 1))
  on conflict(id) do nothing; return new;
end; $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();

create or replace function public.create_couple_invite() returns public.couples language plpgsql security definer set search_path = public as $$
declare result public.couples;
begin
  if auth.uid() is null then raise exception 'Not authenticated'; end if;
  if exists(select 1 from public.couples where status='active' and (user_a=auth.uid() or user_b=auth.uid())) then raise exception 'Already bound to a couple'; end if;
  select * into result from public.couples where user_a=auth.uid() and status='pending' order by created_at desc limit 1;
  if result.id is null then
    insert into public.couples(user_a, invite_code, invite_expires_at)
    values(auth.uid(), upper(substr(replace(gen_random_uuid()::text,'-',''),1,8)), now()+interval '1 hour') returning * into result;
  else
    update public.couples set invite_code=upper(substr(replace(gen_random_uuid()::text,'-',''),1,8)), invite_expires_at=now()+interval '1 hour'
    where id=result.id returning * into result;
  end if; return result;
end; $$;

create or replace function public.bind_couple_by_invite(p_invite_code text) returns public.couples language plpgsql security definer set search_path = public as $$
declare result public.couples;
begin
  if auth.uid() is null then raise exception 'Not authenticated'; end if;
  if exists(select 1 from public.couples where status='active' and (user_a=auth.uid() or user_b=auth.uid())) then raise exception 'Already bound to a couple'; end if;
  update public.couples set user_b=auth.uid(), status='active', invite_code=null, invite_expires_at=null
  where upper(invite_code)=upper(trim(p_invite_code)) and status='pending' and user_b is null and user_a<>auth.uid() and invite_expires_at>now()
  returning * into result;
  if result.id is null then raise exception 'Invalid or expired invite code'; end if; return result;
end; $$;

create or replace function public.get_time_capsules() returns table(
  id uuid, couple_id uuid, creator_id uuid, title text, content text, unlock_date date, reminder_enabled boolean,
  content_types text[], created_at timestamptz, updated_at timestamptz, locked boolean
) language sql security definer set search_path = public as $$
  select t.id,t.couple_id,t.creator_id,t.title,case when t.unlock_date<=current_date then t.content else null end,t.unlock_date,
    t.reminder_enabled,t.content_types,t.created_at,t.updated_at,t.unlock_date>current_date
  from public.time_capsules t where public.is_active_couple_member(t.couple_id) order by t.unlock_date asc;
$$;

alter table public.photo_collections enable row level security;
alter table public.diary_attachments enable row level security;
alter table public.custom_tags enable row level security;
alter table public.time_capsules enable row level security;
drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_self_or_partner" on public.profiles for select to authenticated using(
  id=auth.uid() or exists(select 1 from public.couples c where c.status='active' and ((c.user_a=auth.uid() and c.user_b=profiles.id) or (c.user_b=auth.uid() and c.user_a=profiles.id)))
);
create policy "photo_collections_select_member" on public.photo_collections for select to authenticated using(public.is_active_couple_member(couple_id));
create policy "photo_collections_insert_owner" on public.photo_collections for insert to authenticated with check(uploader_id=auth.uid() and public.is_active_couple_member(couple_id));
create policy "photo_collections_update_owner" on public.photo_collections for update to authenticated using(uploader_id=auth.uid()) with check(uploader_id=auth.uid() and public.is_active_couple_member(couple_id));
create policy "photo_collections_delete_owner" on public.photo_collections for delete to authenticated using(uploader_id=auth.uid());
create policy "diary_attachments_select_member" on public.diary_attachments for select to authenticated using(public.is_active_couple_member(couple_id));
create policy "diary_attachments_insert_owner" on public.diary_attachments for insert to authenticated with check(uploader_id=auth.uid() and public.is_active_couple_member(couple_id));
create policy "diary_attachments_delete_owner" on public.diary_attachments for delete to authenticated using(uploader_id=auth.uid());
create policy "custom_tags_member_all" on public.custom_tags for all to authenticated using(public.is_active_couple_member(couple_id)) with check(public.is_active_couple_member(couple_id));
create policy "time_capsules_member_insert" on public.time_capsules for insert to authenticated with check(creator_id=auth.uid() and public.is_active_couple_member(couple_id));
create policy "time_capsules_member_update" on public.time_capsules for update to authenticated using(public.is_active_couple_member(couple_id)) with check(public.is_active_couple_member(couple_id));
create policy "time_capsules_member_delete" on public.time_capsules for delete to authenticated using(public.is_active_couple_member(couple_id));
revoke select on public.time_capsules from authenticated;
grant execute on function public.create_couple_invite() to authenticated;
grant execute on function public.bind_couple_by_invite(text) to authenticated;
grant execute on function public.get_time_capsules() to authenticated;

drop policy if exists "couples_update_member" on public.couples;
create or replace function public.update_couple_started_at(p_started_at date)
returns public.couples language plpgsql security definer set search_path = public as $$
declare result public.couples;
begin
  update public.couples set started_at=p_started_at
  where status='active' and (user_a=auth.uid() or user_b=auth.uid()) returning * into result;
  if result.id is null then raise exception 'Active couple not found'; end if;
  return result;
end; $$;
grant execute on function public.update_couple_started_at(date) to authenticated;

create or replace function public.update_time_capsule(p_id uuid,p_title text,p_content text,p_unlock_date date,p_reminder_enabled boolean,p_content_types text[])
returns public.time_capsules language plpgsql security definer set search_path = public as $$
declare result public.time_capsules;
begin
  update public.time_capsules set title=p_title,content=p_content,unlock_date=p_unlock_date,
    reminder_enabled=p_reminder_enabled,content_types=coalesce(p_content_types,'{}')
  where id=p_id and public.is_active_couple_member(couple_id) returning * into result;
  if result.id is null then raise exception 'Time capsule not found'; end if;
  return result;
end; $$;
create or replace function public.delete_time_capsule(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
begin delete from public.time_capsules where id=p_id and public.is_active_couple_member(couple_id); end; $$;
grant execute on function public.update_time_capsule(uuid,text,text,date,boolean,text[]) to authenticated;
grant execute on function public.delete_time_capsule(uuid) to authenticated;
create or replace function public.set_time_capsule_reminder(p_id uuid,p_enabled boolean)
returns void language plpgsql security definer set search_path = public as $$
begin update public.time_capsules set reminder_enabled=p_enabled where id=p_id and public.is_active_couple_member(couple_id); end; $$;
grant execute on function public.set_time_capsule_reminder(uuid,boolean) to authenticated;

drop policy if exists "notifications_insert_own" on public.notifications;
revoke insert on public.notifications from authenticated;
create or replace function public.notify_comment_target() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.notifications(user_id,type,title,content,target_type,target_id)
  select member_id,'comment','新的评论',new.content,new.target_type,new.target_id
  from (select c.user_a member_id from public.couples c where c.id=new.couple_id
        union all select c.user_b from public.couples c where c.id=new.couple_id) members
  where member_id is not null and member_id<>new.author_id;
  return new;
end; $$;
drop trigger if exists on_comment_notify on public.comments;
create trigger on_comment_notify after insert on public.comments for each row execute function public.notify_comment_target();

insert into storage.buckets(id,name,public) values('avatars','avatars',false),('photos','photos',false),('diary-attachments','diary-attachments',false)
on conflict(id) do update set public=false;
create policy "couple_storage_read" on storage.objects for select to authenticated using(
  bucket_id in ('avatars','photos','diary-attachments') and public.is_active_couple_member(((storage.foldername(name))[1])::uuid)
);
create policy "couple_storage_insert" on storage.objects for insert to authenticated with check(
  bucket_id in ('avatars','photos','diary-attachments') and public.is_active_couple_member(((storage.foldername(name))[1])::uuid)
  and ((storage.foldername(name))[2])::uuid=auth.uid()
);
create policy "couple_storage_delete" on storage.objects for delete to authenticated using(
  bucket_id in ('avatars','photos','diary-attachments') and owner_id=auth.uid()::text
);

-- Deliver the tables already subscribed to by src/api/realtimeApi.js through
-- Supabase Realtime. The check makes this safe to apply after a partial manual
-- Dashboard setup: a table already present in the publication is left alone.

do $$
declare
  target_table text;
begin
  if not exists (select 1 from pg_publication where pubname = 'supabase_realtime') then
    raise exception 'The supabase_realtime publication is required before enabling application Realtime tables';
  end if;

  foreach target_table in array array[
    'couples',
    'diaries',
    'diary_attachments',
    'photo_collections',
    'photos',
    'anniversaries',
    'custom_tags',
    'time_capsules',
    'comments',
    'notifications'
  ]
  loop
    if not exists (
      select 1
      from pg_publication_tables
      where pubname = 'supabase_realtime'
        and schemaname = 'public'
        and tablename = target_table
    ) then
      execute format('alter publication supabase_realtime add table public.%I', target_table);
    end if;
  end loop;
end;
$$;

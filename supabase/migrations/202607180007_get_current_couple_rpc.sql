-- Resolve the active relationship through a controlled read path.
-- This keeps the relationship bootstrap independent from direct table-select
-- quirks while still returning only the caller's own active relationship.

create or replace function public.get_current_couple()
returns public.couples
language sql
stable
security definer
set search_path = public
as $$
  select c
  from public.couples c
  where auth.uid() is not null
    and c.status = 'active'
    and (c.user_a = auth.uid() or c.user_b = auth.uid())
  order by c.updated_at desc, c.created_at desc
  limit 1;
$$;

revoke all on function public.get_current_couple() from public;
revoke all on function public.get_current_couple() from anon;
grant execute on function public.get_current_couple() to authenticated;

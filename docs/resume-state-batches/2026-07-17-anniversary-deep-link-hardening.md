# 2026-07-17 Anniversary Deep-link Hardening

## Scope

Continued Phase 2 Real-data hardening on `codex/phase2-real-data` from commit `343275bc5256423e11309212c0c4d21c2eb5773a`.

## Completed

- Removed fake empty-store countdown content from `app/anniversary/template.js`.
- The template page no longer invents `相识纪念日`, `18` days, or the hard-coded date `2026.06.28`.
- Added an explicit empty state that still permits template preview and routes users to create a real anniversary.
- Added static regression checks for both anniversary countdown and template deep links.
- Confirmed the existing anniversary editor uses Real API write methods and does not fall back to mock writes in Real mode.

## Commits in this batch

- `e2fe1af96aab0cccee3b89fb9b7bf7e3d8abe76f` — remove fake template countdown data
- `c7e87443e343b3833b6a48ca95e6369d7f29a4e1` — add anniversary deep-link static guards

## Follow-up identified

- `app/anniversary/edit.js` currently treats an unknown `id` as create mode. Add an explicit invalid-edit-target state so a stale or malformed edit deep link cannot create a new anniversary accidentally.
- Continue scanning other detail/edit routes for the same `id supplied but entity missing` behavior.

## Validation status

Not executed in this connector-only environment:

- `npm run test:final`
- `npm run check:web`
- Android export
- `git diff main...HEAD --check`
- Supabase migration dry-run and RLS integration

These remain required before Codex handoff or release readiness.
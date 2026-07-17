# Tags real-mode persistence truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the Tags API path used by `app/tags/index.js`, including create, update, delete, category mapping, returned rows, and Store refresh behavior.

## Changes

- Real mode now requires an explicit supported category instead of silently defaulting to `心情`.
- Real mode no longer invents `pricetag-outline` when the caller did not provide an icon.
- Missing tag IDs are rejected before update or delete.
- Update and delete only report success when Supabase returns the affected row.
- Missing, unauthorized, or already-deleted tags now return an explicit failure.

## Modified files

- `src/api/tagApi.js`

## Static guard

Added `src/__tests__/tagsTruth.static.test.js`.

## Commits

- `3799c0a44995ff7bc36d05723ff752320a32da38` — `fix(tags): harden real-mode tag persistence truth`
- `8f3decdb75a5ad73991f89d6e0eef5434fdb9b7a` — `test(tags): guard real-mode tag persistence truth`

## Validation status

Static test file was added, but no test command was executed in this batch.

Not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

`docs/resume-state.md` was not modified.

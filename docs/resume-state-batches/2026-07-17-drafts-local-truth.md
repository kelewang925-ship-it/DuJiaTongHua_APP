# Draft local-truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the drafts page so Real mode does not present local state as server-persisted drafts.

## Changes

- Real mode explicitly labels drafts as current-device data.
- AI creations are not locally deleted in Real mode.
- Missing descriptions and edit times use explicit unavailable semantics.
- Clear and delete confirmations no longer imply server deletion.

## Static guard

Added `src/__tests__/draftsTruth.static.test.js`.

## Validation status

Static test file was added but no test command was executed in this batch.

Not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

Function commit: `cbb52ff582065e0be2a7a95846632c1c75352670`
Test commit: `61edf805e3b0b0952dba6fdf8569c82322973570`

`docs/resume-state.md` was not modified.
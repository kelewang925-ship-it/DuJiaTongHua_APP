# Mine profile-truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the Mine tab so Real mode does not invent profile, relationship, or membership state.

## Changes

- Real profile fields come from backend profile/couple responses.
- Missing nicknames and relationship fields are disclosed.
- Couple statistics are hidden until a persisted active relationship exists.
- The page no longer labels the user as a member before checking membership state.
- Sign-out failures are surfaced and the dialog no longer promises unsynced data was uploaded.

## Static guard

Added `src/__tests__/mineTruth.static.test.js`.

## Validation status

Static test file was added but no test command was executed in this batch.

Not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

Function commit: `dd7b91175d7ff05f04ec69014514267ddbc83be1`
Test commit: `8d34826444564636f38398b4e0cbe7404cc1b972`

`docs/resume-state.md` was not modified.
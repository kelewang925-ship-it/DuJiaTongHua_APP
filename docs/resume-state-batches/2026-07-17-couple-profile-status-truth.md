# Couple profile status truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the user and couple profile API path for unbound state, missing partner profiles, relationship status, date validation, and update confirmation.

## Changes

- Missing authenticated user and malformed couple rows now fail explicitly.
- Unbound state remains explicit and does not invent a partner profile.
- Missing partner profile is disclosed through `partnerProfileAvailable`.
- Relationship status remains null when the backend did not provide it.
-恋爱开始日期 is strictly validated.
- Couple profile update only succeeds when the backend returns a persisted couple row.

## Modified files

- `src/api/coupleApi.js`

## Static guard

Added `src/__tests__/coupleProfileTruth.static.test.js`.

## Commits

- `c2b7c2ad54e7ba411ac5f0ed9ad529b861cd9360` — `fix(profile): harden couple profile status truth`
- `3092cf843c2c418322e69a5e9f81949ebb8f446c` — `test(profile): guard couple profile status truth`

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

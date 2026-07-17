# Invite binding result truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited invite generation and binding API semantics for code validation, expiry metadata, persisted couple identity, and relationship status.

## Changes

- Invite codes must match the supported uppercase alphanumeric format.
- Generated invite responses are rejected when the code is missing or malformed.
- Invalid expiry metadata is reported instead of displayed as valid.
- Binding no longer reports success merely because the RPC returned without an error.
- A persisted couple ID is required before `bound: true` is returned.
- Explicit non-active relationship results are treated as not yet bound.

## Modified files

- `src/api/coupleApi.js`

## Static guard

Added `src/__tests__/inviteBindingTruth.static.test.js`.

## Commits

- `df382eced030afdeb6fe477750a4c180cd57e01e` — `fix(invite): verify real binding results`
- `caa03c4370631785165a185f5f9fe624daa12c89` — `test(invite): guard real binding result truth`

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

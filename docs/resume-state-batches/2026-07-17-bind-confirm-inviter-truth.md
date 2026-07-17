# Bind confirmation inviter truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the binding confirmation page so unverified route parameters and design assets do not impersonate a real inviter.

## Changes

- Validates invite-code format before binding.
- Replaces the design avatar with an explicit unavailable placeholder.
- Does not present a route nickname as verified identity.
- Requires `bound` and a persisted couple ID before success.
- Distinguishes confirmed binding from a subsequent refresh failure.

## Static guard

Added `src/__tests__/bindConfirmTruth.static.test.js`.

## Validation status

Static test file was added but no test command was executed in this batch.

Not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

`docs/resume-state.md` was not modified.
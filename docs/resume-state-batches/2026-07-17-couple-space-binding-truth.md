# Couple space binding-truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the couple space so Real mode only renders an active persisted relationship and backend-provided profile fields.

## Changes

- Binding now requires a persisted couple ID, active status, and persisted partner ID.
- Missing nicknames, start dates, statuses, and anniversary fields use explicit unavailable semantics.
- Invalid or future start dates do not produce a fake day count.
- The unsupported comment shortcut was removed from the generic quick links.
- Empty timeline copy now reflects real data availability.

## Static guard

Added `src/__tests__/coupleSpaceTruth.static.test.js`.

## Validation status

Static test file was added but no test command was executed in this batch.

Not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

Function commit: `06d25d70d6b952df1e7117b65501166eb246aa8e`
Test commit: `a4303f0341417bed786f0b1281a8d3eddba238e4`

`docs/resume-state.md` was not modified.
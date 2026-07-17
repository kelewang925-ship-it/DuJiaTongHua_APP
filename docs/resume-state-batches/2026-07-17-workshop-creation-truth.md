# Workshop creation-truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the workshop history so Real mode only exposes backend-provided creation metadata and valid targets.

## Changes

- Missing source, style, title, status, and artwork are no longer replaced with business-like defaults.
- Creation rows without backend IDs are not navigable.
- Result navigation requires an actual result URL; otherwise it opens the job progress route.
- Empty history explicitly states that no real creations are available.

## Static guard

Added `src/__tests__/workshopTruth.static.test.js`.

## Validation status

Static test file was added but no test command was executed in this batch.

Not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

Function commit: `fe3b217630bbded53ce9f2072b083e48e3996009`
Test commit: `b6a6744bb0a3c52d4a44e80722167e3780d2ca21`

`docs/resume-state.md` was not modified.
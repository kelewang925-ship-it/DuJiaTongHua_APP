# Photo-to-comic source truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited photo-to-comic so Real mode does not present design illustrations as user photos or simulated AI output.

## Changes

- Isolates design-photo options to Mock mode.
- Real mode only considers records with IDs and actual image URLs.
- Shows an explicit empty state when no usable photos exist.
- Does not render design art as a Real-mode result preview.
- Prevents Real mode from creating local AI tasks or success claims.

## Static guard

Added `src/__tests__/photoToComicTruth.static.test.js`.

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
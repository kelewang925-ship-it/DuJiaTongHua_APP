# Text-to-comic source truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited text-to-comic so missing diary content is not replaced with an invented story or fake diary metadata.

## Changes

- Removes the fallback story.
- Disables diary selection when no real diary content exists.
- Discloses missing diary title and date.
- Separates Mock preview artwork from Real mode.
- Prevents Real mode from creating local AI tasks.

## Static guard

Added `src/__tests__/textToComicTruth.static.test.js`.

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
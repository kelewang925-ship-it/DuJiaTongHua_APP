# Story detail target-truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the couple story detail route so it requires a real timeline target and a valid comment target.

## Changes

- Missing route IDs no longer fall back to the first timeline item.
- Missing title, time, and description fields use explicit unavailable semantics.
- Comment navigation is disabled unless the story maps to a real record ID and supported target type.
- Missing parameters and missing records are distinguished.

## Static guard

Added `src/__tests__/storyDetailTruth.static.test.js`.

## Validation status

Static test file was added but no test command was executed in this batch.

Not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

Function commit: `0f0d4e74290298bd688cad8b8604957d02fb1859`
Test commit: `55e97c44aaa083b3d188a3544815029a63c0db44`

`docs/resume-state.md` was not modified.
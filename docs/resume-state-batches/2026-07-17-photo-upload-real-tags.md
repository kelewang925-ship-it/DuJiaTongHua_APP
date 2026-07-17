# Photo upload real-mode tag hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited `app/photo/upload.js` for Real-mode business data defaults.

## Finding

The upload form initialized every new collection with the `约会` tag, including Real mode. During save, an empty selection was also replaced with a synthetic `照片` tag. Neither value came from the user or backend, so persisted collections could contain fabricated classifications.

## Changes

- Moved the demo `约会` default into `mockDefaultTags`.
- Real mode now starts with no selected tags.
- Persistence now sends the exact `selectedTags` array without adding a fallback tag.
- Marked the tag field as optional.
- Added `src/__tests__/photoUpload.static.test.js`.

## Validation status

Static test source was added but no test command was executed in this batch.

The following remain unexecuted:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

## Resume constraints

- Continue only on `codex/phase2-real-data`.
- Do not modify `main`.
- Do not overwrite `docs/resume-state.md`.
- Do not claim Phase 2 is complete.

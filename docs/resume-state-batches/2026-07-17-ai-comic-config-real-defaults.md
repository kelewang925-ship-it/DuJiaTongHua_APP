# AI comic config real-mode defaults guard

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited `app/ai/comic-config.js` for demo data and business-completion wording leaking into Real mode.

## Findings

- Real mode prefilled a fictional comic title and prompt.
- Real mode also appeared to have a photo source selected without a real entity selection.
- The page stated an estimated generation duration and that work would continue after leaving, despite Real-mode generation being unavailable.
- Privacy and quality copy sounded like active server behavior.

## Changes

- Added explicit `mockDraft` values and only apply them in Mock mode.
- Real mode now starts with empty title, empty prompt, and no selected source.
- Mock task creation requires a source plus non-empty title and prompt.
- Mock creation status and button wording are explicitly labelled as local demonstration behavior.
- Removed unsupported generation-duration and background-processing claims.
- Clarified that privacy and quality settings are not active service guarantees in Real mode.

## Static guard

Added `src/__tests__/comicConfig.static.test.js`.

The test has not been executed in this session.

## Validation status

Not run:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

This note does not claim phase completion.

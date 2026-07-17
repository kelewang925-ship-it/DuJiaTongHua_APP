# Comments backend identity truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited the Comments API path for target validation, author profile return data, ordering, create confirmation, and delete confirmation.

## Changes

- Real mode only accepts supported diary and photo target types.
- Invalid or missing targets fail explicitly before querying.
- Newly created comments now request the persisted author profile from Supabase.
- Comment creation only succeeds when a backend row with an ID is returned.
- Delete only succeeds when the owned comment row is actually returned.
- Comments are loaded newest first using backend timestamps.

## Modified files

- `src/api/commentApi.js`

## Static guard

Added `src/__tests__/commentsTruth.static.test.js`.

## Commits

- `5564f17e2f110b75dc4aba6bb6f7c90b03881d2f` — `fix(comments): preserve backend comment identity`
- `89460ee2f67b2d356e19f117a34b1b12c537d930` — `test(comments): guard backend comment identity`

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

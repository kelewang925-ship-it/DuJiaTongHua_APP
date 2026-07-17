# Search real-result truth hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Hardened `app/search.js` so Real mode does not invent missing summaries, dates, source names, styles, or visual covers.

## Changes

- Missing anniversary descriptions remain empty.
- AI result descriptions only use fields returned by data sources.
- Missing AI style/source/status fields are no longer replaced with `童话绘本`, `童话工坊`, or magic-status copy.
- Missing and invalid creation dates remain absent.
- Result dates are rendered only when present.
- Real results use category placeholders instead of unrelated design cover artwork.
- Missing summaries are explicitly marked as unavailable.
- Empty-result copy no longer implies hidden story content.

## Static guard

Added `src/__tests__/searchTruth.static.test.js`.

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

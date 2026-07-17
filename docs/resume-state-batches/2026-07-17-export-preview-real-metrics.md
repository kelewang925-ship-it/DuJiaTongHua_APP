# Export preview real-metric guards

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Completed

- Removed the forced minimum of 8 preview pages.
- Removed the forced minimum of 6.2 MB.
- Photo counts now treat missing `photoCount` as zero instead of three.
- Empty selected content now renders an empty state.
- Export and share actions are disabled when there is no real content.
- Chapter samples are created only for selected sections with matching records.
- Added `src/__tests__/exportPreview.static.test.js`.

## Still pending

- Clean fixed custom date text and missing photo count fallback in `app/data/pdf-export.js`.
- Inspect remaining export and backup surfaces.
- Run `npm run test:final`.
- Run `npm run check:web`.
- Run `git diff main...HEAD --check`.
- Android validation.
- Supabase migration dry-run and RLS validation.

`ready_for_codex_validation = no`

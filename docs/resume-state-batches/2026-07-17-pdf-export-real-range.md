# PDF export real range guards

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Completed

- Removed fabricated photo count fallback (`photoCount || 3`).
- Missing photo counts now contribute zero.
- Removed the hardcoded custom range `2022.05.20 ～ 2026.07.16`.
- Added a loaded date range derived from records, creations, and anniversaries.
- Custom range now explicitly reports that no dates have been selected.
- Empty content categories are disabled.
- Preview navigation is blocked when the selected real item count is zero.
- Preview parameters only include content categories with real loaded items.
- Removed unsupported member/export-success wording from the configuration page.

## Tests added

- `src/__tests__/pdfExport.static.test.js`

## Commits

- `20bb288d8054090bf771a196a9a4b1c432a85e43`
- `0af3df3fa829c9cb1f1bdc97ac3ffbc08a0d7672`

## Validation status

Not run yet:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

Do not mark phase complete.

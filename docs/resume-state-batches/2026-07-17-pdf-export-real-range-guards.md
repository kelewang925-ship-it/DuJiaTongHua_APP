# PDF export real range guards

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Completed

- Removed fabricated photo count fallback from `app/data/pdf-export.js`.
- Loaded date range is derived from real diary, creation, and anniversary timestamps.
- Removed fixed custom date text (`2022.05.20 ～ 2026.07.16`).
- Default export range is now `all`, which can be resolved from loaded entities.
- Custom range remains explicitly unset until a real date-range selector exists.
- Preview navigation is blocked when custom dates are unset.
- Empty content types are disabled and excluded from preview params.
- Capability copy no longer claims real PDF, download, watermark, or print support when unavailable.

## Tests

Updated:

- `src/__tests__/pdfExport.static.test.js`

The test now guards photo counts, fixed dates, real loaded-range derivation, empty selections, unset custom dates, and non-empty included sections.

## Validation status

Not run in this connector session:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

Do not mark Phase 2 complete until these validations are actually executed.

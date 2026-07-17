# Diary detail and share preview deep-link guards

Branch: `codex/phase2-real-data`

## Completed

- `app/diary/detail.js`
  - resolves diary by route `id`
  - requires `type === '日记'`
  - renders an empty state for missing or stale links
  - removes first-record fallback, fixed title fallback and default tag injection
  - carries diary id into edit, text-to-comic and share routes
  - removes debug logging

- `app/share-preview.js`
  - resolves target by route `id` and `type`
  - supports record-backed and creation-backed previews
  - renders an empty state when target is missing
  - removes first-record fallback and fabricated nickname, date and place metadata
  - disables unavailable privacy fields

## Regression tests

- `src/__tests__/diaryDetail.static.test.js`
- `src/__tests__/sharePreviewTarget.static.test.js`

## Validation status

Not phase complete. Still required:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

# Photo Album Real-Data Truth Hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited `app/photo/album.js` for fabricated counts, labels, covers, and local-only deletion in Real mode.

## Findings

- Missing `photoCount` values were displayed as 3 photos.
- Empty tags were displayed as the fabricated `照片` tag.
- Missing or failed Real-mode images were replaced with decorative design-system covers, which could look like actual uploaded content.
- Delete always called the local Mock-only `removePhotoRecord` action even though `deletePhotoReal` already existed.

## Changes

- Added a numeric `getPhotoCount` helper; missing counts now display `数量未记录` and contribute zero to totals.
- Removed fallback `照片` tags from cards and timeline entries.
- Decorative fallback covers are now Mock-only. Real mode renders an explicit missing/unavailable image state.
- Real mode deletion now awaits `deletePhotoReal` and keeps the record visible when the API reports failure.
- Delete dialog and toast copy now distinguish Real cloud deletion from local Mock deletion.
- Added `src/__tests__/photoAlbum.static.test.js`.

## Validation Status

Static test source was added but not executed in this batch.

The following were not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

Phase 2 remains in progress.

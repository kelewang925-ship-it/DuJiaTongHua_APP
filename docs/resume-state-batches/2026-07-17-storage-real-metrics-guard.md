# Storage page real-metrics guard

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Hardened `app/data/storage.js` so the page no longer presents estimated storage usage or simulated cache-cleaning success as real product state.

## Changes

- Removed the fixed 10 GB quota and all calculated GB usage values.
- Removed the fallback that counted every photo record as three photos when `photoCount` was missing.
- Removed minimum fake sizes for empty photo and AI collections.
- Derived diary, photo collection, photo and creation counts from the currently loaded store entities.
- Treat missing or invalid photo counts as zero.
- Removed the local-only cache size state and the success receipt that claimed cache deletion had completed.
- Disabled cache cleanup until a real device cache scan/delete API is available.
- Added explicit UI copy explaining that capacity and cache management are not yet connected.

## Tests added

- `src/__tests__/storagePage.static.test.js`

The static guard rejects fake count fallbacks, minimum GB estimates and local simulated cleanup success.

## Validation status

Not run in this batch:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

This batch does not mark Phase 2 complete.

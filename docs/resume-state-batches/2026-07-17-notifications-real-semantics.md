# Notifications real-semantics hardening

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Hardened `app/notifications/index.js` so Real mode no longer invents notification semantics or navigation affordances.

## Changes

- Unknown backend notification types now display as `其他` instead of being forced into `互动`.
- Missing subjects and timestamps remain absent instead of receiving fallback story copy.
- Real notices without a verified route display `仅通知` instead of a chevron.
- Loading/error states no longer claim that the inbox has no unread items.
- Mark-all avoids a backend write when there are no unread notifications.
- Empty-state copy now describes the actual filter state.
- Footer distinguishes server-backed notices from Mock demo notices.

## Static guard

Added `src/__tests__/notificationsTruth.static.test.js`.

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

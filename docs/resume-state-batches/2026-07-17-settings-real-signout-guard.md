# Settings real sign-out guard

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Hardened `app/settings.js` so leaving the account performs a real authentication sign-out instead of only navigating to the login screen.

## Changes

- Calls `signOut()` from `src/api/authApi.js`.
- Stops navigation when sign-out fails and surfaces the API error.
- Calls `resetForSession(null)` only after successful sign-out to clear session-scoped in-memory business data and realtime state.
- Prevents duplicate sign-out actions while the request is running.
- Reworded local theme, notification and privacy switches so they are not presented as persisted server settings.
- Updated the logout confirmation copy to distinguish session cleanup from deletion of server data.

## Static guard

Added `src/__tests__/settingsLogout.static.test.js` covering:

- use of the auth sign-out API;
- failure handling before navigation;
- session store reset ordering;
- non-persistent wording for local preview controls.

## Commits

- `5527a09eea7a07484759cd38a4aa2c7dfca4c94c` — settings implementation
- `1f4e2797181f4da350f8aa750d0b54da1bce396a` — static test

## Validation status

Not run in this connector session:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

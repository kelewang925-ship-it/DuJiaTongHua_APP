# AI character profile Real-mode default guard

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited `app/ai/character-profile.js` for fabricated identity and persistence behavior.

## Finding

The page correctly blocked Real-mode saves, but it still initialized Real mode with demo names and a demo description:

- 林小满
- 陆星河
- 喜欢散步、热可可和把普通日子写成故事

Those values were then displayed as the profile used for generation, which could be mistaken for loaded user data.

## Changes

- Moved all demo values into `mockProfile`.
- Added an empty Real-mode profile.
- Selected initial values by API mode.
- Added empty preview copy for Real mode.
- Kept Mock-mode save wording explicitly local and demonstrative.
- Kept Real-mode save blocked with no simulated success state.

## Static coverage

Added `src/__tests__/characterProfile.static.test.js` to guard mode-specific defaults and Real-mode persistence wording.

## Validation

Static test file was added but no test command was executed in this batch.

## Remaining validation

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

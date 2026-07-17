# 2026-07-17 Story and Comic Deep-Link Guards

## Branch

`codex/phase2-real-data`

## Completed

- Hardened `app/couple/story-detail.js`.
  - Reads the requested timeline item by route `id`.
  - Uses the first real timeline item only when no `id` was supplied.
  - Shows an explicit empty state when the record is missing.
  - Removed the fake `第 428 天的小故事`, `刚刚`, and demo description fallbacks.
  - Passes the real story id to the comments route.
  - Real mode still blocks simulated like success.

- Hardened `app/ai/comic-result.js`.
  - A missing or unauthorized work now renders an empty state.
  - Removed the built-in demo title, static three-beat story, and static triptych preview.
  - Story beats and preview assets are rendered only when present on the selected creation.
  - Share preview receives the real creation id.

- Extended `src/__tests__/phase2StaticGuards.test.js` with entity-detail assertions.

## Commits

- `2c70843ec656bd27860d4f867063a66e3a21c768` — story detail guard
- `0cb07d2aa52638f97d7de6069505e0619b317bfd` — comic result guard
- `1ad19f27efe357b31bd778bcd0a78f937b836511` — static regression tests

## Validation status

Static source contents were re-fetched after each update. Full local commands remain pending:

```text
npm run test:final
npm run check:web
git diff main...HEAD --check
```

Android export validation and Supabase integration validation remain pending.

`ready_for_codex_validation=no`

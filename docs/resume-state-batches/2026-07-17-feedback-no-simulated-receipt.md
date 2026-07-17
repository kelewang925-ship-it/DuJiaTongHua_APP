# Feedback simulated receipt guard

Date: 2026-07-17
Branch: `codex/phase2-real-data`

## Scope

Audited `app/help-feedback.js` for local-only actions presented as submitted feedback.

## Problems removed

- Generated a fake `TH-xxxxxx` ticket from `Date.now()`.
- Stored a local `submitted` receipt without an API response.
- Cleared the user's description and contact fields after local handling.
- Displayed `反馈已收进 Mock 信箱` and `已收件` despite no persistence.
- Presented attachment interaction without an upload implementation.

## Current behavior

- Real mode clearly states that feedback submission is unavailable.
- Mock-capable mode only validates the draft form and preserves all input.
- No ticket, receipt, accepted state, or success toast is generated.
- Attachment entry explicitly states that no file is selected or uploaded.
- Capability checks receive the resolved API mode.

## Static guard

Added `src/__tests__/helpFeedback.static.test.js` to reject simulated ticket IDs, receipt state, field clearing, and upload claims.

## Validation status

The static test file was added but no test command was executed in this batch.

Not executed:

- `npm run test:final`
- `npm run check:web`
- `git diff main...HEAD --check`
- Android validation
- Supabase migration dry-run
- Supabase RLS validation

`docs/resume-state.md` was not modified in this batch.

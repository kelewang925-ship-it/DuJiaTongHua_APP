# Overlay entry focus implementation plan

> Execute inline with superpowers:executing-plans. Preserve the full114-page goal.

**Goal:** Keep form context visible when a sheet opens in a short viewport, while preserving safe cancellation, Tab order, editing and persistence.

**Architecture:** Change only the initial focus decision in the existing shared modal. Ordinary form dialogs autofocus their programmatically focusable heading; dialogs containing a marked Danger action retain the existing safe action focus. Keep the existing scroll container, focus trap, navigation, dirty guard and field components.

**Spec:** design-html/prototype/ACCEPTANCE_REQUIREMENTS.md and INTERACTION_RULES.md.

**Constraints:** Local HTML/JS mock only; no changes to the original D workspace; no RN/API work; browser viewport reduction is simulated keyboard pressure, not real-device IME evidence. Do not promote final acceptance from this batch.

## Steps

- [x] Reproduce the clipped heading with actual pet-task entry at five widths and420px height.
- [x] Repair ordinary-form entry focus without changing Danger defaults or form values.
- [x] Execute16 actual form entries at five widths: entry title, heading-to-field Tab order, long textarea content and scrolling, reduced viewport, actual save and parent save where applicable.
- [x] Verify non-form/Danger defaults, clean Escape and trigger focus restoration.
- [x] Refresh all114 canonical initial pages after the shared JS change, then bind results to current source and archive prior coverage.
- [x] Update issues, interaction/acceptance documents and progress; commit the verified batch.

## Review focus

1. A programmatic heading focus must not open an editable field automatically.
2. Danger content must keep cancellation as its initial action.
3. Heading tabindex=-1 must not add a repeated stop to the Tab loop.
4. Long text and shrinking viewport must not lose edits or make save unreachable.
5. Closing must restore the connected trigger; real mobile keyboard/screen-reader behavior remains a separate gate.

Ruling: Reverse Tab from the newly focused heading escaped the native dialog in the intermediate implementation. Add the heading to the existing Shift+Tab boundary and prove it with the same five-width failure/pass cycle before the final114-page replay.

Verification: final form/default-focus84/84; fresh initial570/570 and114 keyboard pages; danger/primary23/23; repairs5/5; runtime228 observations/1696 controls with0 errors/unbound; catalog114 pages/267 assets. Real IME and remaining full flows are explicitly outside this batch acceptance.

# Component and token coverage audit plan

> Execute inline using executing-plans; keep the full114-page objective.

**Goal:** Inspect actual rendered shared components and computed shared tokens on114 pages in the existing empty/populated fixtures, and bind static local declarations and controller call candidates.

**Architecture:** Reuse the current catalog, runtime seeds and route queries. Inspect DOM classes and computed CSS without changing production. Keep controller call sites distinct from observed rendering, and count local CSS literals as audit candidates rather than automatically treating artwork as defects. Missing use in these fixtures does not prove a hidden condition has no component.

**Tech Stack:** Python, HTMLParser, Playwright and current native HTML/CSS/JS.

- [x] Scan all114 HTML/controller/stylesheet dependencies, component call candidates and token declarations.
- [x] Observe228 actual page states at390×844, binding actual routes, shared component counts and computed tokens.
- [x] Generate per-page14-component coverage and token variation/gap records; identify concrete next implementation targets.
- [x] Verify unchanged source/current752 initial evidence and commit the audit. This is coverage evidence, not final flow/layout acceptance.

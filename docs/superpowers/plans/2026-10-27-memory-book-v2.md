# Memory Book V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Implement the approved tactile memory-book module with a swipeable shelf, readable mobile page turning and consistent creation/editing/organizing screens.

**Architecture:** Retain PrototypeBooks, existing editor sessions and all 21 route identities. Replace m08 presentation through local HTML/CSS plus focused shelf/reader components; extend stable reading anchors compatibly. Use semantic DOM for paper content and segmented CSS 3D page geometry for curved turning without a new runtime dependency.

**Tech Stack:** Existing vanilla HTML/CSS/JavaScript, shared PrototypeUI, Python Playwright and installed Chrome.

**Spec:** docs/superpowers/specs/2026-10-27-memory-book-redesign-design.md (user approved implementation in chat on 2026-10-27).

## Global Constraints

- Work only on codex/design-html-rebuild; preserve other workspace changes.
- Scope presentation changes to m08; retain custom/pages generation convention and existing route/query contracts.
- Reuse existing sources, privacy, backups, draft/dirty/conflict rules and UI feedback. No simulated cloud success.
- Body 16/26, accessible 48 logical pixel actions, five mobile widths, landscape and reduced motion.
- Full-page mockup images are references only; actual UI must be editable DOM, with actual user images preserved.
- No new runtime dependency; existing Python browser tools are available via .design-html-tools.

## Review Focus

1. Long text and large fonts must remain readable through continuations, never cut off or shrink.
2. Carousel selection and continue/open actions must target the selected stable book ID.
3. Canceled drags, orientation changes and mode switches must preserve current content without premature writes.
4. Private/deleted sources and cross-window changes must invalidate visible and preloaded content.
5. Organization drafts must survive failures and reject stale writes without editing source records.

### Task 1: New behavior contracts and baseline

**Files:** Create design-html/prototype/verify_book_v2.py; use existing book_test_helpers.py.
**Interfaces:** Browser pages exercise actual PrototypeBooks data and semantic controls; report isolated evidence under evidence/{baseline,current}/book-v2/.

- [x] Write cases for carousel selection, same-document reading, continuation/large text, drag cancel, privacy refresh, organizer and five-width layouts.
- [x] Run new contracts against current implementation and preserve expected failures.
- [x] Run existing verify_book_flow.py baseline and confirm its current behavior.

### Task 2: Shared module presentation and swipeable shelf

**Files:** Create assets/prototype-book-v2.css, assets/prototype-book-v2.js and prototype/build_book_v2.py; modify custom/m08-p01..21.html and generated pages equivalents; add focused assets/book-v2/ textures if needed.
**Interfaces:** build_book_v2.build() emits consistent semantic page scaffolding before existing controllers; PrototypeBookV2.shelf(ctx) renders existing book collection, selected ID and scroll-snap navigation; cover(container,book) composes real DOM title and existing theme/photo.

- [x] Preserve controller-required selectors and labels in semantic templates; reuse existing controller behavior and shared styles.
- [x] Implement scroll-snap shelf, selected book information, continuation, all-books/drafts/archive navigation and genuine empty states.
- [x] Run shelf and full creation contracts; inspect 390px shelf screenshot.

### Task 3: Single-scene tactile reader

**Files:** Create assets/prototype-book-reader.js and local reader styles; modify prototype-book.js/read dispatch and prototype-book-store.js/read.
**Interfaces:** PrototypeBookReader.render(ctx,current,n) consumes B.pageView; read(id,pageId,anchor?) stores compatible lastPage plus optional text/block anchor. Reader owns only local navigation and pagination, not original records.

- [x] Build measured text/image continuations, portrait single/landscape double sheets, current anchor and same-document URL updates.
- [x] Implement segmented curved turn, drag/rebound, boundary buttons, cover opening/closing, keyboard and reduced-motion alternative.
- [x] Connect chapter/thumbnail/bookmark sheet, image viewer, supplement tools and continuous large-text mode; respect privacy and save failures.
- [x] Run reading/long-content/cancel/orientation/privacy contracts, existing reading/state/image tests and inspect static/midturn screenshots.

### Task 4: Organizer and associated page polish

**Files:** Modify prototype-book-structure.js and local V2 presentation; retain existing specialist editor sessions and route contracts.
**Interfaces:** Organizer renders existing chapters/pages and B.structure guarded transaction; thumbnails open existing typed editor; drag and menu update the same uncommitted array.

- [x] Add semantic chapter grid, actual page previews, drag reorder with menu alternatives, sticky save/add/manage actions and draft protection.
- [x] Apply V2 layout to basic info, cover/theme, source selection, templates, editors, completion, directory, supplement and management routes.
- [x] Run existing flow/structure/editor-draft/supplement/privacy contracts and all 21 routes at five widths.

### Task 5: Review, evidence and delivery

**Files:** Create prototype/BOOK_V2_IMPLEMENTATION.md; update only new design/plan status and relevant README entry.
**Interfaces:** Current evidence records source fingerprints and actual executed cases, without changing unrelated page acceptance claims.

- [x] Run browser checks, JS syntax, custom/pages identity and scoped changed-file inspection; capture actual shelf/reader/organizer screenshots.
- [x] Independent final code review, fix meaningful findings, rerun affected checks.
- [x] Deliver preview entry, changes and verified limits. Real-phone performance and human visual acceptance remain explicit pending items.

## Execution ledger

2026-10-27: User authorized immediate implementation; inline execution chosen by agent to avoid unnecessary dispatches. Existing linked worktree reused. No runtime install is required. Plan interfaces reviewed: preparation precedes old render; shelf/reader replace only their presentation; organizer retains the guarded save transaction. No known interface conflict.

2026-10-28: Tasks 1–5 complete. 159 browser checks passed (11 V2 contracts, 7 integration/touch/motion, 106 layouts, 35 existing business regressions). Independent review findings fixed and rechecked. Five JS syntax checks, 21 route pairs, scoped diff and resource checks passed. Evidence: design-html/prototype/evidence/current/book-v2/verification-summary.json. Ruling: keep existing named branch/worktree and uncommitted changes for review; no merge/push requested.

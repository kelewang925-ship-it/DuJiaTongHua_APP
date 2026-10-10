# Identity deletion implementation plan

> Execute inline with executing-plans. Keep the full 114-page goal active.

**Goal:** Verify account and pet identity deletion, invalid input, dirty cancellation, persistent boundaries and failure recovery; fix confirmed data-loss behavior.

**Architecture:** Reuse source-bound observed entry selectors and independent existing fixtures in fresh Chrome contexts. Inject actual one-shot storage quota failure without replacing production functions. Compare full snapshots and unrelated sentinel keys; preserve failing evidence before repairs. Any production change requires historical evidence to be clearly distinguished from current evidence.

**Tech Stack:** Python, Playwright, plain JavaScript and browser storage.

- [x] Execute twelve cases: two entries × success, blank, wrong identity, dirty cancellation, semantic failure/retry, quota failure/retry.
- [x] Diagnose and repair confirmed issues, retaining baselines and exact scope.
- [x] Revalidate affected flows and classify older evidence honestly after any source changes.
- [x] Document priority issues, evidence and remaining requirements; commit.

## Evidence

Baseline 61684 exited 1 (6/12; unstable busy-label locator); corrected baseline 17299 exited 1 (11/12; account quota failure lost storage). Production fixed. First repaired run 30502 exited 0 (12/12), final extended run 57110 exited 0 (13/13, includes second-write rollback). Settings 21905 exited 0 (81), runtime 25614 exited 0 (228 observations), onboarding 30781 exited 0 (82). Onboarding initial preflight exited 1 without executing cases due stale runtime, rerun only after runtime refresh. Product/source, scripts/reports and baseline hashes are bound. Prior evidence retained and demoted; 163 current and 589 historical initial controls, 0 final accepted pages.

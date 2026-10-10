# Current initial controls refresh plan

> Execute inline using executing-plans; preserve the full 114-page objective.

**Goal:** Re-execute six remaining modules after the account deletion repair: 589 initial controls and their 26 existing supplementary cases.

**Architecture:** Keep production frozen. Run existing browser validators sequentially to avoid the known parallel preparation interference, recording actual child exit codes and source/report/script hashes. Preserve overwritten reports and catalog. Retain current 82 onboarding and 81 settings checks from the preceding phase, without rerunning unchanged evidence.

**Tech Stack:** Python subprocess orchestration, existing Playwright validators and simple local HTML.

- [x] Preserve reports and run record109, moment55, time54, workshop92, pet151, book154 (615 checks including 589 initial).
- [x] Resolve concrete failures with original diagnostics; do not broaden timeouts or silently skip cases.
- [x] Rebuild catalog and verify 752 current initial controls, current execution provenance and retained identity13 evidence.
- [x] Update progress artifacts and commit. Hidden operations and final acceptance remain pending.

## Live execution handoff

Parent unified execution session 85141 is confirmed live. Record finished with actual child exit0: 109/109 (92 initial); moment finished with actual child exit0: 55/55 (46 initial). Both report hashes/source fingerprints are recorded in remaining-initial-refresh-source.json. The same parent started time and is producing passing cases; workshop, pet and book follow sequentially. Poll this exact session; do not restart from a timeout or from this plan alone. Production remains frozen. Rebuild catalog only after all reports are terminal, then invoke verify_remaining_initial_refresh.py with the actual parent session and observed exit0. No complete-phase checkpoint or final acceptance claim has been made.

Next continuation verified the same live handle: time finished54/54 exit0 and workshop92/92 exit0. Total310/615 passed, with284 newly replayed initial controls; report hashes and unchanged source are recorded by the runner. It started pet, then book follows. Parent85141 is still live, not terminal; do not launch duplicate validators or rebuild the catalog yet. After actual terminal success, run build_page_contracts.py and then verify_remaining_initial_refresh.py --parent-session 85141 --parent-exit 0, followed by verify_page_contracts.py. Update docs/checkpoint only after inspecting results and commit the phase. Older identity checkpoint's catalog snapshot is retained at pre-remaining-refresh-97edd42, and the new verifier checks its exact hash while retaining the unchanged13 identity/81 settings/82 onboarding evidence.

## Terminal evidence

Parent85141 exited0; all six child exits0,615/615 checks passed,589 initial. Catalog rebuilt:752 current initial,0 historical. Exact scripts/reports/source, retained13 identity/81 settings/82 onboarding and archived163-control phase catalog snapshot validated. Full catalog verifier passes114/267/228/1696/41 with0 final accepted pages. No product changes or timeout changes. Complete phase checkpoint binds actual parent exit.

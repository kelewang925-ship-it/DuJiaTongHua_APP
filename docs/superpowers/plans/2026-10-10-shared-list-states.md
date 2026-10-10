# Shared list Empty/Error adoption

Reuse existing components.state and preserve action labels, routes, filter state, data stores and refresh/retry. Scope: 10 existing data-loader error branches; search, diary (normal/draft/filtered), filtered photo, capsule (three tabs), workshop (empty/favorites), draft box and pet timeline empties. Keep independent illustrated empty design pages.

- [x] Capture baseline from actual named contexts, without changing the simulated request timers.
- [x] Adopt shared Empty/Error in these branches, retaining module classes and all original actions; bound pet status component to its overlay.
- [x] Verify 22 contexts at five widths, CTA routes/filter restore/dialog and failure retry with actual data restoration and storage preservation.
- [x] Update current/historical evidence and commit. Full product flow and visual acceptance remain open.

Final state run: session94742 exit0, 110/110; Loading regression: session93604 exit0, 30/30. Baseline session94829 exit1, 0/22. Global runtime/catalog refresh explicitly pending after consolidated component adoption.

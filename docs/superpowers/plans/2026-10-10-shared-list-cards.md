# Dynamic list Card adoption

Reuse the existing Card factory. Add optional node content to preserve module markup (photo thumbnails, title/excerpt/date/privacy, reply CTA and metadata) with native button/article semantics. Preserve route callbacks, image fallback and reminder/reply read updates. Module classes retain original media/grid/row layout; the component supplies the common card foundation. Scope: 13 renderers across home/search/diary/photo/moment/anniversary/reminder/capsule/workshop recent/list/draft box/pet timeline/replies.

- [x] Capture original dynamic-card and factory-content baseline.
- [x] Add optional content nodes to the current factory without changing its existing title/message API; adopt it in all 13 renderers.
- [x] Verify actual route/read behavior, image/text preservation, five-width hit targets and Enter; relevant shared state regression.
- [x] Record current/historical fingerprints and scope-specific layout reasons, then commit. Full visual/flow acceptance remains open.

Actual execution: baseline76437 exit1 (0/14), first product75973 exit1 (60/66), first replay66433 exit1 (61/66), final reminder replay14266 exit0 (66/66 combined, 61 retained and 5 fresh). One syntax preflight exited1 with zero browser cases before final replay. State regression53702 exit0 (110/110). Product stayed frozen throughout all post-implementation checks.

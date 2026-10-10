# Shared list Loading adoption

Implement inline. Reuse existing `PrototypeUI.components.loading`, preserve original labels, 400ms simulated request, error/retry and list behavior. Scope: search, diary, photo, moment, anniversary, capsule, workshop, draft box, pet and pet life load functions. No API or navigation changes.

- [x] Observe a failing baseline with real transient DOM and empty/populated/failure-retry conditions.
- [x] Replace local loading content with shared skeletons in the 10 data-load functions.
- [x] Verify transient status, aria-busy, original refresh disable/restore, error recovery, and updated runtime inventory; preserve old fingerprint evidence as historical.
- [x] Update coverage gaps and implementation evidence, commit verified work.

Measured follow-up: pet growth Skeleton had zero-width child bars at all five widths. Scoped pet-load width/paragraph-flow correction and fresh final evidence are included. The preliminary runtime scan was deliberately stopped for this concrete production correction; the final scan uses the final frozen source.

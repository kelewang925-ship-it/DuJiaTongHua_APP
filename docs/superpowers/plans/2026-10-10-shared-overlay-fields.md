# Shared editable overlay fields

Reuse components.field in settings/pet life/book edit helpers, moment replies and pet care notes. Add select options to the existing field factory, style select with the same field foundation, and route fieldError to the field's associated inline error when available. Preserve old explicit error targets, unrelated Toast errors, values, limits, labels, guard and persistence logic. Original inline canvas forms are a separate later migration.

- [x] Capture original field adoption/select/error baseline using old locator candidates as search hints and real current execution as proof.
- [x] Adopt shared fields in five current renderers/helpers and extend select/error association without a new framework.
- [x] Verify 14 overlay entries at five widths: associated labels/errors, invalid correction, duplicate save, quota rollback/retry and actual stored results; identity deletion regression.
- [x] Record provenance/current scope, document remaining original canvas fields, commit verified work.

Actual execution: baseline30409 exit1 (0/15); fields28357 exit0 (71/71); identity73204 exit1 (10/13: three old Toast assertions), inline replay62213 exit0 (3 fresh+10 retained=13). Production stayed frozen during current checks.

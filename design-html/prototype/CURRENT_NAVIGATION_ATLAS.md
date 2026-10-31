# 当前导航与条件案例索引

覆盖114页、393条初态实际跳转、110个手动弹层入口，以及153个记录明确最终页面的业务案例。

实线是初态单次操作的跨页结果；虚线弹层表示已观察入口；菱形表示多步案例及最终落点。共享案例关联多个控件时，不将最终页认定为每个控件的一次点击结果。

[关系图](CURRENT_NAVIGATION_ATLAS.mmd)／[完整机器索引](evidence/current/navigation-atlas-20261101.json)／[逐控件业务规则](CURRENT_HIDDEN_CONTROL_BEHAVIORS.md)。

每项保留原报告路径、行号和SHA256。报告没有明确终点的关闭、字段候选、筛选或本地状态另列，不猜测页面目标，也不将其认定为死路。此索引整理既有实际结果，没有重新运行浏览器。

采集后HTML／JavaScript／资源的字节必须仍相同；CSS差异逐项保留旧／新指纹，结合[同值Token证明](CURRENT_STYLE_TOKEN_ADOPTION.md)及[照片热区修复](CURRENT_QUALITY_REFRESH.md)查阅。原报告不改绑。

## 条件案例最终落点

| 来源上下文 | 案例条件／操作 | 最终页 | 报告行 |
| --- | --- | --- | --- |
| m08-p05 | 101 / exact photo reference saved in coverPhoto only after parent save | m08-p06 | [0](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p09 | 108 / exact diary reference saved in source only after parent save | m08-p13 | [1](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p09 | 109 / exact photo reference saved in photoSource only after parent save | m08-p13 | [2](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 112 / exact photo reference saved in photos only after parent save | m08-p13 | [3](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 113 / exact photo reference saved in photos only after parent save | m08-p13 | [4](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 114 / exact photo reference saved in photos only after parent save | m08-p13 | [5](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p11 | 116 / exact photo reference saved in photoSource only after parent save | m08-p13 | [6](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p11 | 117 / exact moment reference saved in source only after parent save | m08-p13 | [7](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p12 | 119 / exact work reference saved in source only after parent save | m08-p13 | [8](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p12 | 120 / exact pet reference saved in source only after parent save | m08-p13 | [9](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p12 | 121 / exact photo reference saved in photoSource only after parent save | m08-p13 | [10](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 111 / photo operation remains candidate until parent save; exact replacement/crop/removal and last-photo recovery verified | m08-p13 | [11](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 111 / photo operation remains candidate until parent save; exact replacement/crop/removal and last-photo recovery verified | m08-p13 | [12](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 111 / photo operation remains candidate until parent save; exact replacement/crop/removal and last-photo recovery verified | m08-p13 | [13](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 115 / exact sticker saved once after parent save | m08-p13 | [14](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 115 / exact sticker saved once after parent save | m08-p13 | [15](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 115 / exact sticker saved once after parent save | m08-p13 | [16](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m08-p10 | 115 / exact sticker saved once after parent save | m08-p13 | [17](evidence/current/hidden-business-20261101-final/verify_book_v2_hidden_editors/results.json) |
| m03-p07 | success / diary-delete | m03-p06 | [0](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m03-p07 | semantic-retry / diary-delete | m03-p06 | [1](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m03-p07 | quota-retry / diary-delete | m03-p06 | [2](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m03-p08 | success / diary-delete | m03-p06 | [3](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m03-p08 | semantic-retry / diary-delete | m03-p06 | [4](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m03-p08 | quota-retry / diary-delete | m03-p06 | [5](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m03-p12 | success / photo-delete | m03-p09 | [6](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m03-p12 | semantic-retry / photo-delete | m03-p09 | [7](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m03-p12 | quota-retry / photo-delete | m03-p09 | [8](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p03 | success / moment-delete | m04-p02 | [9](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p03 | semantic-retry / moment-delete | m04-p02 | [10](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p03 | quota-retry / moment-delete | m04-p02 | [11](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p10 | success / anniversary-delete | m04-p07 | [12](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p10 | semantic-retry / anniversary-delete | m04-p07 | [13](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p10 | quota-retry / anniversary-delete | m04-p07 | [14](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p11 | success / anniversary-delete | m04-p07 | [15](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p11 | semantic-retry / anniversary-delete | m04-p07 | [16](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p11 | quota-retry / anniversary-delete | m04-p07 | [17](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p14 | success / capsule-delete | m04-p12 | [18](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p14 | semantic-retry / capsule-delete | m04-p12 | [19](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p14 | quota-retry / capsule-delete | m04-p12 | [20](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p15 | success / capsule-delete | m04-p12 | [21](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p15 | semantic-retry / capsule-delete | m04-p12 | [22](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m04-p15 | quota-retry / capsule-delete | m04-p12 | [23](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p03 | success / work-delete | m05-p09 | [24](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p03 | semantic-retry / work-delete | m05-p09 | [25](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p03 | quota-retry / work-delete | m05-p09 | [26](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p04 | success / work-delete | m05-p09 | [27](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p04 | semantic-retry / work-delete | m05-p09 | [28](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p04 | quota-retry / work-delete | m05-p09 | [29](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p05 | success / work-delete | m05-p09 | [30](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p05 | semantic-retry / work-delete | m05-p09 | [31](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p05 | quota-retry / work-delete | m05-p09 | [32](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p08 | success / work-delete | m05-p09 | [33](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p08 | semantic-retry / work-delete | m05-p09 | [34](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m05-p08 | quota-retry / work-delete | m05-p09 | [35](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | success / settings-tag | m06-p05 | [36](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | semantic-retry / settings-tag | m06-p05 | [37](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | quota-retry / settings-tag | m06-p05 | [38](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | success / settings-tag | m06-p05 | [39](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | semantic-retry / settings-tag | m06-p05 | [40](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | quota-retry / settings-tag | m06-p05 | [41](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | success / settings-tag | m06-p05 | [42](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | semantic-retry / settings-tag | m06-p05 | [43](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p05 | quota-retry / settings-tag | m06-p05 | [44](evidence/current/hidden-business-20261101-final/verify_confirmed_deletions/confirmed-deletion-results.json) |
| m06-p08 | success / settings-account-delete | m01-p01 | [0](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m06-p08 | blank / settings-account-delete | m06-p08 | [1](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m06-p08 | wrong / settings-account-delete | m06-p08 | [2](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m06-p08 | dirty-cancel / settings-account-delete | m06-p08 | [3](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m06-p08 | semantic-retry / settings-account-delete | m01-p01 | [4](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m06-p08 | quota-retry / settings-account-delete | m01-p01 | [5](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m06-p08 | quota-late-retry / settings-account-delete | m01-p01 | [6](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m07-p25 | success / pet-delete | m07-p04 | [7](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m07-p25 | blank / pet-delete | m07-p25 | [8](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m07-p25 | wrong / pet-delete | m07-p25 | [9](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m07-p25 | dirty-cancel / pet-delete | m07-p25 | [10](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m07-p25 | semantic-retry / pet-delete | m07-p04 | [11](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m07-p25 | quota-retry / pet-delete | m07-p04 | [12](evidence/current/hidden-business-20261101-final/verify_identity_deletions/identity-deletion-results.json) |
| m04-p03 | save | m04-p03 | [0](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m04-p03 | quota-retry | m04-p03 | [1](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m04-p03 | invalid | m04-p03 | [2](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p03 | save | m06-p03 | [3](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p03 | quota-retry | m06-p03 | [4](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p03 | invalid | m06-p03 | [5](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p05 | save | m06-p05 | [6](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p05 | quota-retry | m06-p05 | [7](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p05 | invalid | m06-p05 | [8](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p05 | save | m06-p05 | [9](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p05 | quota-retry | m06-p05 | [10](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p05 | invalid | m06-p05 | [11](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p07 | save | m06-p07 | [12](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p07 | quota-retry | m06-p07 | [13](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p08 | save | m06-p08 | [14](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p08 | quota-retry | m06-p08 | [15](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p08 | invalid | m06-p08 | [16](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p08 | save | m06-p08 | [17](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p08 | quota-retry | m06-p08 | [18](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p08 | invalid | m06-p08 | [19](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p12 | save | m06-p12 | [20](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p12 | quota-retry | m06-p12 | [21](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m06-p12 | invalid | m06-p12 | [22](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p11 | save | m07-p11 | [23](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p11 | quota-retry | m07-p11 | [24](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p11 | invalid | m07-p11 | [25](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p18 | save | m07-p18 | [26](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p18 | quota-retry | m07-p18 | [27](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p18 | invalid | m07-p18 | [28](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p19 | save | m07-p18 | [29](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p19 | quota-retry | m07-p18 | [30](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p19 | invalid | m07-p19 | [31](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p19 | save | m07-p19 | [32](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p19 | quota-retry | m07-p19 | [33](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p19 | invalid | m07-p19 | [34](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p25 | save | m07-p25 | [35](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p25 | quota-retry | m07-p25 | [36](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m07-p25 | invalid | m07-p25 | [37](evidence/current/hidden-business-20261101-final/verify_overlay_form_saves/overlay-form-save-results.json) |
| m08-p13 | page-down-save | m08-p14 | [0](evidence/current/hidden-business-20261101/verify_book_v2_hidden_edges/results.json) |
| m08-p13 | move-without-other-chapter-feedback | m08-p13 | [1](evidence/current/hidden-business-20261101/verify_book_v2_hidden_edges/results.json) |
| m08-p13 | delete-last-chapter-empty-cta | m08-p08 | [2](evidence/current/hidden-business-20261101/verify_book_v2_hidden_edges/results.json) |
| m08-p01 | library-tabs | m08-p01 | [0](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p01 | library-open-published | m08-p15 | [1](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | menu-mode-roundtrip | m08-p16 | [6](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | menu-type-roundtrip | m08-p16 | [7](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | menu-organize | m08-p13 | [8](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | menu-cover | m08-p05 | [9](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | menu-manage | m08-p21 | [10](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | menu-shelf | m08-p01 | [11](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | directory-chapter-page | m08-p16 | [13](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | directory-thumbnail-page | m08-p16 | [14](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | directory-bookmarked-page | m08-p16 | [15](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | zoom-controls-return | m08-p16 | [18](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p16 | zoom-privacy-refresh | m08-p16 | [19](evidence/current/hidden-business-20261101/verify_book_v2_hidden_reading/results.json) |
| m08-p13 | chapter-up-save | m08-p14 | [0](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | chapter-down-save | m08-p14 | [1](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | chapter-rename-save | m08-p14 | [2](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | chapter-add-validation-save | m08-p14 | [3](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | chapter-rename-cancel | m08-p13 | [4](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | chapter-boundary-feedback | m08-p13 | [5](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | page-boundary-feedback | m08-p13 | [6](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | page-target-cancel | m08-p13 | [7](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | chapter-move-delete-cancel-failure-retry | m08-p14 | [9](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m08-p13 | page-order-delete-bookmark-cleanup | m08-p14 | [10](evidence/current/hidden-business-20261101/verify_book_v2_hidden_structure/results.json) |
| m07-p04 | empty-state CTA navigates to m07-p02 without writing data | m07-p02 | [7](evidence/current/hidden-business-20261101/verify_hidden_auxiliary_outcomes/results.json) |
| m04-p04 | empty-state CTA navigates to m03-p05 without writing data | m03-p05 | [8](evidence/current/hidden-business-20261101/verify_hidden_auxiliary_outcomes/results.json) |
| m01-p07 | phone-recovery / auth | m01-p04 | [0](evidence/current/hidden-business-20261101/verify_hidden_choice_outcomes/results.json) |
| m01-p07 | phone-register / auth | m01-p03 | [1](evidence/current/hidden-business-20261101/verify_hidden_choice_outcomes/results.json) |
| m06-p07 | logout preserves content and session fields; clears login flag/challenge; welcome page reached | m01-p01 | [5](evidence/current/hidden-business-20261101/verify_hidden_settings_pet_outcomes/results.json) |
| m06-p08 | logout preserves content and session fields; clears login flag/challenge; welcome page reached | m01-p01 | [6](evidence/current/hidden-business-20261101/verify_hidden_settings_pet_outcomes/results.json) |
| m07-p24 | care paused; identity/inventory/growth retained; settings page reached | m07-p25 | [22](evidence/current/hidden-business-20261101/verify_hidden_settings_pet_outcomes/results.json) |
| m05-p02 | source / exact radio/checkbox source consumed; new draft for start action, existing editors defer write until explicit parent draft save | m05-p03 | [6](evidence/current/hidden-business-20261101/verify_hidden_workshop_outcomes/results.json) |
| m05-p04 | photos / exact radio/checkbox source consumed; new draft for start action, existing editors defer write until explicit parent draft save | m05-p09 | [7](evidence/current/hidden-business-20261101/verify_hidden_workshop_outcomes/results.json) |
| m05-p05 | diary / exact radio/checkbox source consumed; new draft for start action, existing editors defer write until explicit parent draft save | m05-p09 | [8](evidence/current/hidden-business-20261101/verify_hidden_workshop_outcomes/results.json) |
| m05-p05 | photo / exact radio/checkbox source consumed; new draft for start action, existing editors defer write until explicit parent draft save | m05-p09 | [9](evidence/current/hidden-business-20261101/verify_hidden_workshop_outcomes/results.json) |
| m05-p05 | moment / exact radio/checkbox source consumed; new draft for start action, existing editors defer write until explicit parent draft save | m05-p09 | [10](evidence/current/hidden-business-20261101/verify_hidden_workshop_outcomes/results.json) |
| m05-p06 | cancel-generation / generating work becomes draft with all input/source fields retained; editor reached; other works preserved | m05-p03 | [11](evidence/current/hidden-business-20261101/verify_hidden_workshop_outcomes/results.json) |

另有634个关联报告案例未记录明确最终URL，完整数据见机器索引。它们不能用于推断跨页导航。

## 复验

`python design-html/prototype/build_current_navigation_atlas.py --check`校验所有产物与来源报告、行号、通过状态和字节指纹；采集后的CSS只允许已登记同值替换与两条照片热区样式。Token行为等价性另运行`python design-html/prototype/verify_current_style_tokens.py`。

完整41项目标仍在执行；此图补齐已观察证据的统一入口，不宣称所有条件组合、视觉差异或提交等待边界已经完成。

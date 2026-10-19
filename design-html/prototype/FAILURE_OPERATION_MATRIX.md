# 失败操作执行矩阵

本批30个案例通过，实际触发26个不同失败操作。61个字面量入口中17个已观察、44个尚未追踪。

“已观察”仅证明所列案例中的失败被实际触发，案例完整断言通过；不代表该操作所有权限、取消、并发和布局条件完成。静态测试引用仅用于寻找下一步执行入口。

| 操作 | 当前追踪 | 实际案例 | 静态候选脚本 |
| --- | --- | --- | --- |
| anniversary-delete | 未追踪 |  | verify_anniversary_states.py、verify_confirmed_deletions.py、verify_time_product_journey.py |
| anniversary-load | 未追踪 |  | verify_anniversary_states.py、verify_shared_list_loading.py |
| anniversary-save | 未追踪 |  | verify_time_product_journey.py |
| anniversary-toggle | 未追踪 |  | verify_anniversary_states.py |
| bind | 已观察 | bind-profile-failure-retry | verify_onboarding_controls.py、verify_onboarding_faults.py |
| book-delete | 已观察 | delete-cancel-failure-stable-id | verify_book_states.py |
| book-editor-stash | 未追踪 |  | verify_book_editor_draft.py |
| book-export | 未追踪 |  |  |
| book-load | 已观察 | load-retry-bookmark-persistence | verify_book_error_controls.py、verify_book_states.py |
| capsule-collect | 未追踪 |  | verify_time_product_journey.py |
| capsule-date | 未追踪 |  |  |
| capsule-delete | 未追踪 |  | verify_confirmed_deletions.py、verify_time_product_journey.py |
| capsule-load | 未追踪 |  | verify_shared_list_loading.py |
| capsule-open | 未追踪 |  | verify_time_product_journey.py |
| capsule-save | 未追踪 |  | verify_time_product_journey.py |
| capsule-toggle | 未追踪 |  | verify_time_product_journey.py |
| credentials | 未追踪 |  |  |
| diary-comment | 未追踪 |  | verify_diary_states.py |
| diary-delete | 未追踪 |  | verify_confirmed_deletions.py、verify_diary_states.py、verify_record_controls.py |
| diary-load | 未追踪 |  | verify_diary_states.py、verify_shared_list_loading.py |
| diary-save | 未追踪 |  | verify_native_field_flows.py、verify_record_controls.py |
| invite | 未追踪 |  | verify_onboarding_controls.py |
| login | 未追踪 |  | verify_account_routes.py、verify_onboarding_controls.py、verify_product_journey.py |
| moment-comment | 未追踪 |  |  |
| moment-delete | 未追踪 |  | verify_confirmed_deletions.py、verify_moment_states.py |
| moment-load | 未追踪 |  | verify_moment_states.py、verify_shared_list_loading.py |
| moment-save | 未追踪 |  |  |
| pet-adopt | 已观察 | invite-validation-dirty-failure-reminder | verify_pet_states.py |
| pet-delete | 未追踪 |  | verify_danger_confirmations.py、verify_danger_overlays.py、verify_danger_primary_contract.py、verify_identity_deletions.py、verify_pet_life_states.py |
| pet-export | 未追踪 |  |  |
| pet-life-load | 未追踪 |  | verify_pet_life_states.py、verify_shared_list_loading.py |
| pet-load | 已观察 | load-retry-backup-paused-care | verify_pet_states.py、verify_shared_list_loading.py |
| photo-comment | 已观察 | comment-delete-failure | verify_photo_states.py |
| photo-delete | 已观察 | comment-delete-failure | verify_confirmed_deletions.py、verify_photo_states.py、verify_record_controls.py |
| photo-load | 已观察 | image-display-load-recovery | verify_photo_states.py、verify_shared_list_loading.py |
| photo-save | 未追踪 |  | verify_native_field_flows.py、verify_record_controls.py |
| profile | 已观察 | bind-profile-failure-retry | verify_account_recovery.py、verify_home_counter.py、verify_onboarding_controls.py、verify_onboarding_faults.py |
| record-search | 未追踪 |  | verify_shared_list_loading.py |
| register | 未追踪 |  | verify_onboarding_controls.py、verify_session_invite_recovery.py |
| remind | 未追踪 |  | verify_onboarding_controls.py、verify_pet_controls.py |
| reset | 未追踪 |  | verify_onboarding_controls.py |
| send-code | 未追踪 |  |  |
| settings-account-delete | 已观察 | phone-code-account-delete-retry | verify_identity_deletions.py |
| settings-backup | 已观察 | automatic-backup-save-retry |  |
| settings-drafts-load | 已观察 | drafts-error-motion-setting | verify_shared_list_loading.py |
| settings-export | 未追踪 |  |  |
| settings-logout | 未追踪 |  |  |
| settings-member | 已观察 | member-feedback-failure-persistence |  |
| settings-preference | 未追踪 |  |  |
| settings-profile | 已观察 | profile-avatar-failure-birthday-cancel |  |
| settings-tag | 未追踪 |  | verify_confirmed_deletions.py、verify_settings_controls.py |
| settings-unlink | 已观察 | review-reject-date-failure | verify_settings_states.py |
| settings-update | 未追踪 |  |  |
| two-factor-verify | 已观察 | two-factor-gates-login-retry |  |
| verify | 已观察 | otp-expiry-resend-retry | verify_onboarding_controls.py、verify_onboarding_faults.py |
| work-album | 未追踪 |  |  |
| work-characters | 未追踪 |  |  |
| work-delete | 未追踪 |  | verify_confirmed_deletions.py |
| work-generate | 未追踪 |  | verify_product_journey.py |
| work-load | 未追踪 |  | verify_shared_list_loading.py |
| work-save | 未追踪 |  |  |
| book-bookmark | 已观察 | load-retry-bookmark-persistence | verify_book_states.py |
| book-create | 已观察 | create-validation-dirty-save-retry | verify_book_states.py |
| book-page | 已观察 | page-save-failure-source-private-independent-text | verify_book_editor_draft.py、verify_book_states.py |
| book-theme | 已观察 | theme-dirty-failure | verify_book_cover.py、verify_book_states.py |
| pet-claim | 已观察 | reward-idempotency-note-failure | verify_pet_states.py |
| pet-feed | 已观察 | feed-failure-quota-atomic | verify_pet_states.py |
| pet-note | 已观察 | reward-idempotency-note-failure | verify_pet_states.py |
| pet-remind | 已观察 | invite-validation-dirty-failure-reminder | verify_pet_states.py |
| settings-feedback | 已观察 | member-feedback-failure-persistence |  |

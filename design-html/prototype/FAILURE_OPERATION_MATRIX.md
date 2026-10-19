# 失败操作执行矩阵

本批110个案例通过，实际触发77个不同失败操作。61个字面量入口中61个已观察、0个尚未追踪。

“已观察”仅证明所列案例中的失败被实际触发，案例完整断言通过；不代表该操作所有权限、取消、并发和布局条件完成。静态测试引用仅用于寻找下一步执行入口。

| 操作 | 当前追踪 | 实际案例 | 静态候选脚本 |
| --- | --- | --- | --- |
| anniversary-delete | 已观察 | toggle-load-delete-failure | verify_anniversary_states.py、verify_confirmed_deletions.py、verify_time_product_journey.py |
| anniversary-load | 已观察 | toggle-load-delete-failure | verify_anniversary_states.py、verify_shared_list_loading.py |
| anniversary-save | 已观察 | anniversary-save-failure-retains-input-retry | verify_time_product_journey.py |
| anniversary-toggle | 已观察 | toggle-load-delete-failure | verify_anniversary_states.py |
| bind | 已观察 | bind-profile-failure-retry | verify_onboarding_controls.py、verify_onboarding_faults.py |
| book-delete | 已观察 | delete-cancel-failure-stable-id | verify_book_states.py |
| book-editor-stash | 已观察 | stash-failure-and-resumed-dirty-discard | verify_book_editor_draft.py |
| book-export | 已观察 | book-export-failure-no-download-retry |  |
| book-load | 已观察 | load-retry-bookmark-persistence | verify_book_error_controls.py、verify_book_states.py |
| capsule-collect | 已观察 | collect-failure-idempotence | verify_time_product_journey.py |
| capsule-date | 已观察 | capsule-date-failure-retry-sealed | verify_last_failure_operations.py |
| capsule-delete | 已观察 | toggle-delete-load-failures | verify_confirmed_deletions.py、verify_time_product_journey.py |
| capsule-load | 已观察 | toggle-delete-load-failures | verify_shared_list_loading.py |
| capsule-open | 已观察 | capsule-open-failure-keeps-secret | verify_last_failure_operations.py、verify_time_product_journey.py |
| capsule-save | 已观察 | capsule-save-failure-retains-input | verify_last_failure_operations.py、verify_time_product_journey.py |
| capsule-toggle | 已观察 | toggle-delete-load-failures | verify_time_product_journey.py |
| credentials | 已观察 | credentials-and-login-retry |  |
| diary-comment | 已观察 | comment-delete-failure | verify_diary_states.py |
| diary-delete | 已观察 | comment-delete-failure | verify_confirmed_deletions.py、verify_diary_states.py、verify_record_controls.py |
| diary-load | 已观察 | list-failure-retry-refresh | verify_diary_states.py、verify_shared_list_loading.py |
| diary-save | 已观察 | diary-save-failure-retains-input-retry | verify_native_field_flows.py、verify_record_controls.py |
| invite | 已观察 | invite-failure-retry | verify_onboarding_controls.py、verify_remaining_failure_operations.py |
| login | 已观察 | credentials-and-login-retry | verify_account_routes.py、verify_onboarding_controls.py、verify_product_journey.py、verify_remaining_failure_operations.py |
| moment-comment | 已观察 | moment-comment-failure-retry | verify_remaining_failure_operations.py |
| moment-delete | 已观察 | cover-quota-delete-recovery | verify_confirmed_deletions.py、verify_moment_states.py |
| moment-load | 已观察 | list-load-refresh-retry | verify_moment_states.py、verify_shared_list_loading.py |
| moment-save | 已观察 | moment-save-failure-retains-input-retry |  |
| pet-adopt | 已观察 | invite-validation-dirty-failure-reminder | verify_pet_states.py |
| pet-delete | 已观察 | settings-load-time-delete-retry | verify_danger_confirmations.py、verify_danger_overlays.py、verify_danger_primary_contract.py、verify_identity_deletions.py、verify_pet_life_states.py |
| pet-export | 已观察 | pet-export-failure-no-download-retry |  |
| pet-life-load | 已观察 | settings-load-time-delete-retry | verify_pet_life_states.py、verify_shared_list_loading.py |
| pet-load | 已观察 | load-retry-backup-paused-care | verify_pet_states.py、verify_shared_list_loading.py |
| photo-comment | 已观察 | comment-delete-failure | verify_photo_states.py |
| photo-delete | 已观察 | comment-delete-failure | verify_confirmed_deletions.py、verify_photo_states.py、verify_record_controls.py |
| photo-load | 已观察 | image-display-load-recovery | verify_photo_states.py、verify_shared_list_loading.py |
| photo-save | 已观察 | photo-save-failure-retains-input-retry | verify_native_field_flows.py、verify_record_controls.py |
| profile | 已观察 | bind-profile-failure-retry | verify_account_recovery.py、verify_home_counter.py、verify_onboarding_controls.py、verify_onboarding_faults.py |
| record-search | 已观察 | search-failure-retry | verify_last_failure_operations.py、verify_shared_list_loading.py |
| register | 已观察 | register-failure-retry | verify_onboarding_controls.py、verify_remaining_failure_operations.py、verify_session_invite_recovery.py |
| remind | 已观察 | remind-failure-retry | verify_onboarding_controls.py、verify_pet_controls.py、verify_remaining_failure_operations.py |
| reset | 已观察 | reset-failure-retry | verify_onboarding_controls.py、verify_remaining_failure_operations.py |
| send-code | 已观察 | send-code-failure-retry | verify_remaining_failure_operations.py |
| settings-account-delete | 已观察 | phone-code-account-delete-retry | verify_identity_deletions.py |
| settings-backup | 已观察 | automatic-backup-save-retry |  |
| settings-drafts-load | 已观察 | drafts-error-motion-setting | verify_shared_list_loading.py |
| settings-export | 已观察 | settings-export-failure-no-download-retry |  |
| settings-logout | 已观察 | logout-failure-keeps-records | verify_remaining_failure_operations.py |
| settings-member | 已观察 | member-feedback-failure-persistence |  |
| settings-preference | 已观察 | preference-failure-retry | verify_remaining_failure_operations.py |
| settings-profile | 已观察 | profile-avatar-failure-birthday-cancel |  |
| settings-tag | 已观察 | tag-failure-retains-input | verify_confirmed_deletions.py、verify_remaining_failure_operations.py、verify_settings_controls.py |
| settings-unlink | 已观察 | review-reject-date-failure | verify_settings_states.py |
| settings-update | 已观察 | version-failure-retry | verify_remaining_failure_operations.py |
| two-factor-verify | 已观察 | two-factor-gates-login-retry |  |
| verify | 已观察 | otp-expiry-resend-retry | verify_onboarding_controls.py、verify_onboarding_faults.py |
| work-album | 已观察 | shared-photo-album-retry |  |
| work-characters | 已观察 | character-failure-dirty-return |  |
| work-delete | 已观察 | history-load-draft-delete-retry | verify_confirmed_deletions.py |
| work-generate | 已观察 | generation-failure-retry-same-work | verify_last_failure_operations.py、verify_product_journey.py |
| work-load | 已观察 | history-load-draft-delete-retry | verify_shared_list_loading.py |
| work-save | 已观察 | long-validation-save-quota |  |
| book-bookmark | 已观察 | load-retry-bookmark-persistence | verify_book_states.py |
| book-create | 已观察 | create-validation-dirty-save-retry | verify_book_states.py |
| book-page | 已观察 | page-save-failure-source-private-independent-text、photo-crop-stickers-roundtrip-save-retry | verify_book_editor_draft.py、verify_book_states.py |
| book-theme | 已观察 | theme-dirty-failure | verify_book_cover.py、verify_book_states.py |
| diary-image | 已观察 | image-recovery-persistence | verify_diary_states.py |
| pet-achievement | 已观察 | achievement-gate-failure-idempotency | verify_pet_life_states.py |
| pet-claim | 已观察 | reward-idempotency-note-failure | verify_pet_states.py |
| pet-feed | 已观察 | feed-failure-quota-atomic | verify_pet_states.py |
| pet-note | 已观察 | reward-idempotency-note-failure | verify_pet_states.py |
| pet-outfit | 已观察 | wardrobe-dirty-save-failure | verify_pet_life_states.py |
| pet-remind | 已观察 | invite-validation-dirty-failure-reminder | verify_pet_states.py |
| pet-room | 已观察 | room-cancel-failure-task | verify_pet_controls.py、verify_pet_life_states.py |
| pet-setting | 已观察 | settings-load-time-delete-retry | verify_pet_life_states.py |
| pet-story | 已观察 | sheet-escape-browser-back-story-failure | verify_pet_controls.py、verify_pet_life_states.py |
| pet-unlock | 已观察 | unlock-shortage-atomic | verify_pet_life_states.py |
| settings-feedback | 已观察 | member-feedback-failure-persistence |  |

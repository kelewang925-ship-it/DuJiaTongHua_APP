# Real data integration checklist

Run only against the dedicated development Supabase project. Use two member
accounts (A/B) and one non-member account (C); never store their passwords in
Git.

1. `npx supabase link --project-ref <ref>`
2. `npx supabase db push --dry-run`
3. `npx supabase db push`
4. Register A/B/C and verify automatic `profiles` rows.
5. Create an invite as A; reject self-bind, invalid and expired codes; bind B;
   reject duplicate binding.
6. For every public table, verify anonymous and C are denied, author ownership
   is enforced, the active partner receives the planned read/write access, and
   disconnected couples lose access.
7. Verify private Storage paths, signed URLs, upload rollback and owner delete.
8. Verify locked capsule content is null before its date and readable after it.
9. Insert a comment as A, verify B receives one notification, mark one/all read,
   and verify Realtime stops after sign-out.

Record the project ref and test result dates in `docs/resume-state.md`; do not
record keys, passwords or access tokens.

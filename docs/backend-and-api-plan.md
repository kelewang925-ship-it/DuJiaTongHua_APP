# Backend and API Plan

## 1. Backend Choice

Recommended backend for MVP:

- Supabase Auth for login and session
- Supabase PostgreSQL for relational data
- Supabase Storage for photos, avatars, comics and videos
- Supabase Edge Functions for AI proxy and async task control
- Supabase Realtime for comments, notifications and AI task progress

This keeps the backend light enough for a React Native frontend developer while still supporting real product growth.

## 2. Architecture

```text
Mobile App
  -> src/api modules
  -> Supabase client or Edge Functions
  -> PostgreSQL / Storage / AI Provider
```

AI calls must never be made directly from the app. API keys should only exist inside server-side functions.

## 3. Supabase SQL Files

### `supabase/schema.sql`

Current status: Phase 5.1 completed.

This file defines the first version of the production database schema. It contains core tables, foreign keys, check constraints, update triggers and commonly used indexes.

Included tables:

- `profiles`
- `couples`
- `diaries`
- `photos`
- `anniversaries`
- `ai_jobs`
- `comments`
- `notifications`

Included shared helpers:

- `public.set_updated_at()` trigger function
- `set_*_updated_at` triggers for tables that have `updated_at`
- `pgcrypto` extension for `gen_random_uuid()`

Important design choices:

- `profiles.id` references `auth.users(id)`.
- Couple-owned content tables all include `couple_id`.
- User-authored tables reference `auth.users(id)` through fields such as `author_id`, `uploader_id`, `creator_id`, or `user_id`.
- AI jobs use constrained `type`, `source_type`, `status`, and bounded `progress` fields.
- Tags and result URLs use Postgres text arrays.
- `character_profile` uses `jsonb` for later AI character settings.

### `supabase/rls-policies.sql`

Current status: Phase 5.2 completed.

This file enables Row Level Security for all core tables and creates the first MVP access rules.

Included helper functions:

- `public.is_active_couple_member(target_couple_id uuid)`
- `public.is_couple_member(target_couple_id uuid)`
- `public.bind_couple_by_invite(p_invite_code text)`

Included RLS coverage:

- `profiles`: users can select, insert and update only their own profile.
- `couples`: members can select their own relationship; authenticated users can create a pending couple as `user_a`; members can update their relationship.
- `diaries`: active couple members can read; only the author can create, update or delete their own diary.
- `photos`: active couple members can read; only the uploader can create, update or delete their own photo rows.
- `anniversaries`: both active couple members can create, read, update and delete shared anniversaries.
- `ai_jobs`: active couple members can read; the creator can create and update their own AI jobs. Service-role Edge Functions can later update progress/results.
- `comments`: active couple members can read; only the author can create, update or delete their own comments.
- `notifications`: users can read, create, update and delete only their own notifications.

Important binding rule:

Directly querying pending invite rows by invite code is not exposed to normal clients. The MVP binding flow should call `public.bind_couple_by_invite(invite_code)` instead.

How to execute in Supabase:

1. Run `supabase/schema.sql` first.
2. Open Supabase SQL Editor.
3. Paste the full content of `supabase/rls-policies.sql`.
4. Run the SQL.
5. In Table Editor, confirm RLS is enabled for all 8 tables.
6. Test with two authenticated users before storing real production data.

Storage note:

`storage.objects` bucket policies are not included yet because buckets may be created from the Supabase dashboard or a later migration. Storage policies must be added before real photo/video/PDF upload is enabled.

---

## 4. Core Tables

### profiles

User profile extension for Supabase Auth.

Fields:
- id uuid primary key, same as auth user id
- nickname text
- avatar_url text
- avatar_text text
- created_at timestamptz
- updated_at timestamptz

### couples

Stores couple relationship.

Fields:
- id uuid primary key
- user_a uuid
- user_b uuid
- started_at date
- invite_code text
- status text: pending, active, disconnected
- created_at timestamptz
- updated_at timestamptz

### diaries

Daily diary records.

Fields:
- id uuid primary key
- couple_id uuid
- author_id uuid
- title text
- content text
- mood text
- tags text array
- cover_photo_url text
- is_private boolean
- created_at timestamptz
- updated_at timestamptz

### photos

Photo records and album items.

Fields:
- id uuid primary key
- couple_id uuid
- uploader_id uuid
- title text
- note text
- file_url text
- thumbnail_url text
- taken_at timestamptz
- tags text array
- created_at timestamptz
- updated_at timestamptz

### anniversaries

Important dates.

Fields:
- id uuid primary key
- couple_id uuid
- title text
- date date
- repeat_type text: none, yearly, monthly
- description text
- template_type text
- created_at timestamptz
- updated_at timestamptz

### ai_jobs

AI generation tasks.

Fields:
- id uuid primary key
- couple_id uuid
- creator_id uuid
- type text: comic, video
- source_type text: diary, photo, text
- source_ids text array
- style text
- character_profile jsonb
- prompt text
- status text: pending, processing, done, failed
- progress int
- result_urls text array
- error_message text
- created_at timestamptz
- updated_at timestamptz

### comments

Couple story comments.

Fields:
- id uuid primary key
- couple_id uuid
- target_type text: diary, photo, ai_creation
- target_id uuid
- author_id uuid
- content text
- created_at timestamptz
- updated_at timestamptz

### notifications

Interaction and system messages.

Fields:
- id uuid primary key
- user_id uuid
- type text
- title text
- content text
- target_type text
- target_id uuid
- read_at timestamptz
- created_at timestamptz
- updated_at timestamptz

## 5. Storage Buckets

Recommended buckets:

- avatars: public or signed read
- photos: private, couple-level access
- ai-comics: private, couple-level access
- ai-videos: private, couple-level access
- exports: private PDF export files

Path rules:

```text
photos/{couple_id}/{user_id}/{photo_id}.jpg
ai-comics/{couple_id}/{job_id}/page-1.png
ai-videos/{couple_id}/{job_id}/result.mp4
exports/{couple_id}/{export_id}.pdf
```

## 6. Auth and Security

Use Supabase Row Level Security.

Rules:

- A user can read their own profile.
- A user can read data only for their active couple.
- A user can create diaries and photos for their own active couple.
- A user can update or delete records authored by themselves.
- AI jobs can be created by either member of the couple.
- Storage objects require signed upload or server-side upload.

Phase 5.2 created table RLS policies. Storage bucket policies are still a separate follow-up before enabling real uploads.

## 7. src/api Module Contract

The frontend should call only `src/api` modules. Pages should not call Supabase directly.

This allows us to keep mock mode during UI development and switch to real backend later.

### Current API mode design

`src/api/client.js` currently owns API mode and shared response helpers.

Current functions:

- `getApiMode()`
- `isMockMode()`
- `delay(ms)`
- `createApiResponse(data, meta)`
- `normalizeError(error, fallbackMessage)`
- `createApiError(error, fallbackMessage)`
- `requestMock(data, ms, meta)`
- `assertRealModeReady()`
- `getSupabaseConfig()`
- `createSupabaseClient()` placeholder for Phase 5

Environment variables:

```bash
EXPO_PUBLIC_API_MODE=mock
EXPO_PUBLIC_SUPABASE_URL=
EXPO_PUBLIC_SUPABASE_ANON_KEY=
EXPO_PUBLIC_APP_NAME=独家童话
```

Response shape:

```js
{
  success: true,
  data: {},
  meta: null,
  error: null,
}
```

Error shape:

```js
{
  success: false,
  data: null,
  meta: null,
  error: {
    message: string,
    code: string,
    raw: unknown,
  },
}
```

## 8. Current API modules

### src/api/diaryApi.js

Purpose:
- Diary list, detail, create, update and delete.

Current functions:
- `getDiaryList(params)`
- `getDiaryDetail(id)`
- `createDiary(payload)`
- `updateDiary(id, payload)`
- `deleteDiary(id)`

Future real implementation:
1. Read current user session.
2. Resolve active `couple_id`.
3. Query or mutate `diaries` table.
4. Return normalized diary object.

### src/api/photoApi.js

Purpose:
- Photo upload and album APIs.

Current functions:
- `getPhotoTimeline(params)`
- `getAlbumList()`
- `uploadPhoto(payload)`
- `getAlbumDetail(albumId)`
- `deletePhoto(id)`

Future real implementation:
1. Request image from Expo ImagePicker.
2. Upload file to Supabase Storage photos bucket.
3. Insert row into photos table.
4. Return normalized photo object.

### src/api/anniversaryApi.js

Purpose:
- Anniversary list, next anniversary, create, update and delete.

Current functions:
- `getAnniversaries()`
- `getAnniversaryList()` compatibility alias
- `getNextAnniversary()`
- `createAnniversary(payload)`
- `updateAnniversary(id, payload)`
- `deleteAnniversary(id)`

### src/api/aiApi.js

Purpose:
- AI comic and video generation.

Current functions:
- `createComicJob(payload)`
- `createVideoJob(payload)`
- `getAiJobDetail(id)`
- `getAiCreationHistory()`
- `retryAiJob(id)`

Future real implementation:
1. Insert ai_jobs row with status pending.
2. Call Edge Function create-ai-comic-job or create-ai-video-job.
3. Edge Function validates user and couple access.
4. Edge Function calls external AI provider.
5. Worker updates status and progress.
6. App polls getAiJobDetail or listens via Realtime.

### src/api/coupleApi.js

Purpose:
- Couple profile, invite code, binding and couple timeline.

Current functions:
- `getCoupleInfo()`
- `getCurrentCouple()` compatibility alias
- `createInviteCode()`
- `bindCouple(inviteCode)`
- `bindCoupleByCode(code)` compatibility alias
- `updateCoupleInfo(payload)`
- `getCoupleTimeline()`

### src/api/storageApi.js

Purpose:
- Storage abstraction for images and generated files.

Current functions:
- `uploadImage(bucket, path, localUri, options)`
- `getSignedUrl(bucket, path, expiresIn)`
- `deleteFile(bucket, path)`

Future real implementation:
1. Upload binary file to Supabase Storage.
2. Return public or signed URL depending on bucket policy.
3. Delete object from Storage when record is deleted.

## 9. Edge Functions

### create-ai-comic-job

Input:
- sourceType
- sourceIds
- text
- style
- characterProfile

Output:
- jobId
- status

Responsibilities:
- Verify user session
- Verify couple access
- Create AI job
- Start generation
- Hide AI provider keys

### create-ai-video-job

Same pattern as comic, but produces video result.

### export-memory-pdf

Responsibilities:
- Select diaries, photos and anniversaries
- Generate PDF server-side
- Upload to exports bucket
- Return signed download URL

## 10. Development Phases

### Phase 1: Frontend Mock

- Current app pages use mock data.
- API modules return requestMock.
- UI and flow are validated first.

### Phase 2: Supabase Integration

- Add Supabase project URL and anon key.
- Replace requestMock with real Supabase queries.
- Keep the same function names.

### Phase 3: Storage and Auth

- Add login page.
- Add profile table.
- Add image upload.
- Add RLS policies.

### Phase 4: AI Tasks

- Add Edge Functions.
- Add ai_jobs table.
- Add polling or Realtime progress.
- Store generated comics and videos.

### Phase 5: Export and Backup

- PDF export
- data backup
- storage management

## 11. Important Rules

- UI pages should never know database details.
- Only `src/api` can talk to backend.
- AI keys must stay server-side.
- Storage paths must include `couple_id`.
- Every table with couple data must include `couple_id`.
- RLS must be enabled before production.
- Mock response shape should match real response shape.
- Mock mode must keep working after real mode is introduced.

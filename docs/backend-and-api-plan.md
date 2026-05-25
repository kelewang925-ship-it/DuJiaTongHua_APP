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

Mobile App
-> src/api modules
-> Supabase client or Edge Functions
-> PostgreSQL / Storage / AI Provider

AI calls must never be made directly from the app. API keys should only exist inside server-side functions.

## 3. Core Tables

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

## 4. Storage Buckets

Recommended buckets:

- avatars: public or signed read
- photos: private, couple-level access
- ai-comics: private, couple-level access
- ai-videos: private, couple-level access
- exports: private PDF export files

Path rules:

photos/{couple_id}/{user_id}/{photo_id}.jpg
ai-comics/{couple_id}/{job_id}/page-1.png
ai-videos/{couple_id}/{job_id}/result.mp4
exports/{couple_id}/{export_id}.pdf

## 5. Auth and Security

Use Supabase Row Level Security.

Rules:

- A user can read their own profile.
- A user can read data only for their active couple.
- A user can create diaries and photos for their own active couple.
- A user can update or delete records authored by themselves.
- AI jobs can be created by either member of the couple.
- Storage objects require signed upload or server-side upload.

## 6. src/api Module Contract

The frontend should call only src/api modules. Pages should not call Supabase directly.

This allows us to keep mock mode during UI development and switch to real backend later.

### src/api/client.js

Purpose:
- Own API mode
- Provide mock delay helper
- Later create Supabase client

Current functions:
- getApiMode()
- delay(ms)
- requestMock(data, ms)

Future functions:
- createSupabaseClient()
- getSession()
- handleApiError(error)

### src/api/mockData.js

Purpose:
- Provide stable mock data for UI development.

Contains:
- mockUser
- mockCouple
- mockPhotos
- mockAiJobs

Future:
- Add mock diaries
- Add mock anniversaries
- Add mock notifications

### src/api/photoApi.js

Purpose:
- Photo upload and album APIs.

Current functions:
- getPhotoTimeline()
- uploadPhoto(payload)
- getAlbumDetail(albumId)

Future real implementation:
1. Request image from Expo ImagePicker.
2. Upload file to Supabase Storage photos bucket.
3. Insert row into photos table.
4. Return normalized photo object.

Expected uploadPhoto payload:

{
  title: string,
  note: string,
  localUri: string,
  tags: string[],
  takenAt: string
}

Expected photo object:

{
  id: string,
  title: string,
  note: string,
  fileUrl: string,
  thumbnailUrl: string,
  date: string,
  tags: string[]
}

### src/api/aiApi.js

Purpose:
- AI comic and video generation.

Current functions:
- createComicJob(payload)
- getAiJobDetail(id)
- getAiCreationHistory()

Future real implementation:
1. Insert ai_jobs row with status pending.
2. Call Edge Function create-ai-comic-job.
3. Edge Function validates user and couple access.
4. Edge Function calls external AI provider.
5. Worker updates status and progress.
6. App polls getAiJobDetail or listens via Realtime.

Expected createComicJob payload:

{
  sourceType: 'diary' | 'photo' | 'text',
  sourceIds: string[],
  text: string,
  style: string,
  characterProfile: object
}

Expected AI job object:

{
  id: string,
  type: 'comic',
  title: string,
  status: 'pending' | 'processing' | 'done' | 'failed',
  progress: number,
  resultUrls: string[],
  errorMessage: string | null
}

### Planned src/api/diaryApi.js

Functions:
- getDiaryTimeline()
- createDiary(payload)
- updateDiary(id, payload)
- deleteDiary(id)
- getDiaryDetail(id)

### Planned src/api/anniversaryApi.js

Functions:
- getAnniversaries()
- createAnniversary(payload)
- updateAnniversary(id, payload)
- deleteAnniversary(id)
- getNextAnniversary()

### Planned src/api/coupleApi.js

Functions:
- getCoupleInfo()
- createInviteCode()
- bindCouple(inviteCode)
- updateCoupleInfo(payload)
- getCoupleTimeline()

### Planned src/api/storageApi.js

Functions:
- uploadImage(bucket, path, localUri)
- getSignedUrl(bucket, path)
- deleteFile(bucket, path)

## 7. Edge Functions

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

## 8. Development Phases

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

## 9. Important Rules

- UI pages should never know database details.
- Only src/api can talk to backend.
- AI keys must stay server-side.
- Storage paths must include couple_id.
- Every table with couple data must include couple_id.
- RLS must be enabled before production.
- Mock response shape should match real response shape.

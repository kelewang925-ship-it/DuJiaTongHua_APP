# Backend Implementation Plan

## 1. Recommended Backend

MVP backend recommendation:

- Supabase Auth for login
- Supabase PostgreSQL for relational data
- Supabase Storage for images and videos
- Supabase Edge Functions for AI API proxy
- Supabase Realtime for comments, likes, notifications and AI job status

This allows the frontend project to move fast without building a full custom backend at the beginning.

Future upgrade path:

- Keep PostgreSQL schema
- Move AI generation to independent Node.js workers if traffic grows
- Add Redis queue for AI tasks
- Add object storage CDN for large media

## 2. Core Data Models

### users

Fields:
- id
- nickname
- avatar_url
- created_at
- updated_at

### couples

Fields:
- id
- user_a_id
- user_b_id
- started_at
- invite_code
- status
- created_at

### diaries

Fields:
- id
- couple_id
- author_id
- title
- content
- mood
- tags
- visibility
- created_at
- updated_at

### photos

Fields:
- id
- couple_id
- uploader_id
- title
- storage_path
- thumbnail_url
- taken_at
- created_at

### albums

Fields:
- id
- couple_id
- title
- description
- cover_photo_id
- created_at

### anniversaries

Fields:
- id
- couple_id
- title
- date
- type
- repeat_rule
- note
- created_at
- updated_at

### ai_creations

Fields:
- id
- couple_id
- creator_id
- type: comic or video
- source_type: diary, photo, text
- source_ids
- style
- prompt
- status: pending, processing, done, failed
- progress
- result_urls
- error_message
- created_at
- updated_at

### comments

Fields:
- id
- target_type
- target_id
- author_id
- content
- created_at

### notifications

Fields:
- id
- user_id
- type
- title
- content
- read_at
- created_at

## 3. Security Rules

The app is private by design. All user data belongs to a couple space.

Rules:
- Users can only read their own profile.
- Users can only read and write data from their bound couple_id.
- Storage files must be scoped by couple_id.
- AI result files must only be visible to the related couple.
- Edge Functions must validate auth session before calling AI providers.

## 4. API Files in src/api

The frontend currently uses mock mode. Each file should be replaced with Supabase calls later.

### src/api/client.js

Purpose:
- Central API mode config
- Shared request helpers
- Later initialize Supabase client here

Future implementation:
- createSupabaseClient
- getSession
- handleApiError
- upload helper

### src/api/mockData.js

Purpose:
- Development mock data
- Enables UI development before backend is ready

Future implementation:
- Keep for storybook/demo mode
- Do not use in production

### src/api/diaryApi.js

Functions:
- createDiary(payload)
- getDiaryList()
- getDiaryDetail(id)

Future backend mapping:
- diaries insert
- diaries select by couple_id
- diaries select detail by id and couple_id

Expected payload for createDiary:
- title
- content
- mood
- tags
- photoIds

### src/api/photoApi.js

Functions:
- getPhotoTimeline()
- uploadPhoto(payload)
- getAlbumDetail(albumId)

Future backend mapping:
- Upload binary to Supabase Storage
- Insert photo metadata into photos table
- Query photos by couple_id ordered by created_at
- Query album detail and related photos

Expected upload payload:
- localUri
- title
- note
- takenAt
- tags

### src/api/anniversaryApi.js

Functions:
- getAnniversaryList()
- createAnniversary(payload)
- updateAnniversary(id, payload)
- deleteAnniversary(id)

Future backend mapping:
- anniversaries CRUD scoped by couple_id
- Calculate countdown on frontend or via database view

Expected payload:
- title
- date
- type
- repeatRule
- note

### src/api/aiApi.js

Functions:
- createComicJob(payload)
- getAiJobDetail(id)
- getAiCreationHistory()

Future backend mapping:
- Insert ai_creations row with pending status
- Call Edge Function to start AI job
- Edge Function calls AI provider without exposing API key
- Update progress and result_urls
- Frontend polls or subscribes through Realtime

Expected createComicJob payload:
- sourceType
- sourceIds
- text
- style
- characterProfile
- ratio

### src/api/coupleApi.js

Functions:
- getCurrentCouple()
- createInviteCode()
- bindCoupleByCode(code)
- getCoupleTimeline()

Future backend mapping:
- couples select by current user
- invite code generation
- bind current user to couple
- timeline query composed from diaries, photos, anniversaries and ai_creations

## 5. Suggested Supabase Buckets

- avatars
- diary-photos
- couple-albums
- ai-comics
- ai-videos
- export-files

## 6. AI Flow

Comic generation flow:

1. Frontend calls createComicJob
2. Backend inserts ai_creations row with pending status
3. Edge Function validates user session and couple_id
4. Edge Function builds AI prompt from selected diary/photo/text
5. AI provider generates comic image or storyboard
6. Result files are uploaded to Storage
7. ai_creations row updates to done
8. Frontend checks progress page and opens result

## 7. Development Phases

Phase 1:
- Keep mock API
- Finish full UI prototype
- Confirm data model

Phase 2:
- Create Supabase project
- Add auth
- Add PostgreSQL schema
- Replace mock APIs gradually

Phase 3:
- Add Storage upload
- Add AI Edge Functions
- Add Realtime progress

Phase 4:
- Add PDF export
- Add backup and restore
- Add notification system

## 8. Backend Completion Checklist

- Auth login works
- Couple binding works
- Diary CRUD works
- Photo upload works
- Album timeline works
- Anniversary CRUD works
- AI comic job works
- AI progress page receives status
- Storage permission rules pass
- Couple data isolation passes
- Export and backup tested

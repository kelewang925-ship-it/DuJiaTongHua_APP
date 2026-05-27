# 《独家童话》后端与 API 规划

> 文档说明：本文档用于规划《独家童话》的后端方案、数据库表结构、Supabase RLS 权限、Storage 存储桶、API 模块契约、Edge Functions、开发阶段和重要后端约束。技术标识如表名、函数名、环境变量和文件路径保持英文，说明内容统一使用中文。

## 1. 后端选择

MVP 阶段推荐使用 Supabase：

- Supabase Auth：用于登录和 session 管理。
- Supabase PostgreSQL：用于关系型业务数据。
- Supabase Storage：用于照片、头像、漫画和视频文件。
- Supabase Edge Functions：用于 AI 代理、异步任务创建和服务端安全逻辑。
- Supabase Realtime：用于评论、通知和 AI 任务进度同步。

这个方案可以让 React Native 前端开发者以较轻的后端成本完成 MVP，同时保留后续真实产品增长所需的能力。

## 2. 整体架构

```text
Mobile App
  -> src/api modules
  -> Supabase client or Edge Functions
  -> PostgreSQL / Storage / AI Provider
```

重要原则：

- AI 服务不能由 App 前端直接调用。
- AI Provider API Key 只能放在服务端函数或后端环境中。
- 页面层不直接知道数据库细节，统一通过 `src/api` 调用。

## 3. Supabase SQL 文件

### `supabase/schema.sql`

当前状态：Phase 5.1 已完成。

该文件定义第一版生产数据库结构，包括核心数据表、外键、检查约束、更新时间触发器和常用索引。

包含表：

- `profiles`
- `couples`
- `diaries`
- `photos`
- `anniversaries`
- `ai_jobs`
- `comments`
- `notifications`

包含共享工具：

- `public.set_updated_at()` trigger function
- 用于有 `updated_at` 字段表的 `set_*_updated_at` triggers
- `pgcrypto` 扩展，用于 `gen_random_uuid()`

关键设计：

- `profiles.id` 对应 `auth.users(id)`。
- 情侣共同拥有的数据表都包含 `couple_id`。
- 用户创建的数据表通过 `author_id`、`uploader_id`、`creator_id` 或 `user_id` 关联 `auth.users(id)`。
- AI 任务使用受约束的 `type`、`source_type`、`status` 和有边界的 `progress` 字段。
- 标签和结果 URL 使用 PostgreSQL text array。
- `character_profile` 使用 `jsonb`，用于后续 AI 人设配置。

### `supabase/rls-policies.sql`

当前状态：Phase 5.2 已完成。

该文件为所有核心表开启 Row Level Security，并创建第一版 MVP 访问规则。

包含辅助函数：

- `public.is_active_couple_member(target_couple_id uuid)`
- `public.is_couple_member(target_couple_id uuid)`
- `public.bind_couple_by_invite(p_invite_code text)`

RLS 覆盖范围：

- `profiles`：用户只能查询、创建和更新自己的 profile。
- `couples`：成员可以查询自己的情侣关系；登录用户可以作为 `user_a` 创建 pending 关系；成员可以更新关系。
- `diaries`：活跃情侣成员可读；只有作者可以创建、更新、删除自己的日记。
- `photos`：活跃情侣成员可读；只有上传者可以创建、更新、删除自己的照片记录。
- `anniversaries`：活跃情侣双方都可以创建、读取、更新、删除共享纪念日。
- `ai_jobs`：活跃情侣成员可读；创建者可以创建和更新自己的 AI 任务。后续 Edge Functions 可用 service role 更新进度和结果。
- `comments`：活跃情侣成员可读；只有作者可以创建、更新、删除自己的评论。
- `notifications`：用户只能读取、创建、更新、删除自己的通知。

重要绑定规则：

- 普通客户端不直接暴露“按邀请码查询 pending invite row”。
- MVP 绑定流程应调用 `public.bind_couple_by_invite(invite_code)`。

Supabase 执行顺序：

1. 先运行 `supabase/schema.sql`。
2. 打开 Supabase SQL Editor。
3. 粘贴完整 `supabase/rls-policies.sql`。
4. 执行 SQL。
5. 在 Table Editor 中确认 8 张核心表均已开启 RLS。
6. 使用两个已登录用户测试权限后，再存储真实生产数据。

Storage 说明：

- 当前还没有包含 `storage.objects` bucket policies。
- Storage buckets 可以通过 Supabase Dashboard 或后续 migration 创建。
- 在启用真实照片、视频、PDF 上传前，必须补充 Storage policies。

---

## 4. 核心数据表

### `profiles`

用户资料扩展表，用于补充 Supabase Auth 用户信息。

字段：

- `id uuid primary key`，与 auth user id 一致。
- `nickname text`
- `avatar_url text`
- `avatar_text text`
- `created_at timestamptz`
- `updated_at timestamptz`

### `couples`

情侣关系表。

字段：

- `id uuid primary key`
- `user_a uuid`
- `user_b uuid`
- `started_at date`
- `invite_code text`
- `status text`：`pending`、`active`、`disconnected`
- `created_at timestamptz`
- `updated_at timestamptz`

### `diaries`

日记记录表。

字段：

- `id uuid primary key`
- `couple_id uuid`
- `author_id uuid`
- `title text`
- `content text`
- `mood text`
- `tags text array`
- `cover_photo_url text`
- `is_private boolean`
- `created_at timestamptz`
- `updated_at timestamptz`

### `photos`

照片记录和相册素材表。

字段：

- `id uuid primary key`
- `couple_id uuid`
- `uploader_id uuid`
- `title text`
- `note text`
- `file_url text`
- `thumbnail_url text`
- `taken_at timestamptz`
- `tags text array`
- `created_at timestamptz`
- `updated_at timestamptz`

### `anniversaries`

重要日期 / 纪念日表。

字段：

- `id uuid primary key`
- `couple_id uuid`
- `title text`
- `date date`
- `repeat_type text`：`none`、`yearly`、`monthly`
- `description text`
- `template_type text`
- `created_at timestamptz`
- `updated_at timestamptz`

### `ai_jobs`

AI 生成任务表。

字段：

- `id uuid primary key`
- `couple_id uuid`
- `creator_id uuid`
- `type text`：`comic`、`video`
- `source_type text`：`diary`、`photo`、`text`
- `source_ids text array`
- `style text`
- `character_profile jsonb`
- `prompt text`
- `status text`：`pending`、`processing`、`done`、`failed`
- `progress int`
- `result_urls text array`
- `error_message text`
- `created_at timestamptz`
- `updated_at timestamptz`

### `comments`

情侣故事评论表。

字段：

- `id uuid primary key`
- `couple_id uuid`
- `target_type text`：`diary`、`photo`、`ai_creation`
- `target_id uuid`
- `author_id uuid`
- `content text`
- `created_at timestamptz`
- `updated_at timestamptz`

### `notifications`

互动和系统消息表。

字段：

- `id uuid primary key`
- `user_id uuid`
- `type text`
- `title text`
- `content text`
- `target_type text`
- `target_id uuid`
- `read_at timestamptz`
- `created_at timestamptz`
- `updated_at timestamptz`

## 5. Storage Buckets

推荐存储桶：

- `avatars`：头像，可公开读或签名读。
- `photos`：照片，私有，按情侣关系控制访问。
- `ai-comics`：AI 漫画结果，私有，按情侣关系控制访问。
- `ai-videos`：AI 视频结果，私有，按情侣关系控制访问。
- `exports`：PDF 导出文件，私有。

路径规则：

```text
photos/{couple_id}/{user_id}/{photo_id}.jpg
ai-comics/{couple_id}/{job_id}/page-1.png
ai-videos/{couple_id}/{job_id}/result.mp4
exports/{couple_id}/{export_id}.pdf
```

## 6. Auth 与安全规则

使用 Supabase Row Level Security。

规则：

- 用户只能读取自己的 profile。
- 用户只能读取自己 active couple 下的数据。
- 用户只能为自己的 active couple 创建日记和照片。
- 用户只能更新或删除自己创建的记录。
- AI 任务可由情侣双方任意一方创建。
- Storage 对象需要签名上传或服务端上传。

Phase 5.2 已创建表级 RLS policies。Storage bucket policies 仍是启用真实上传前的后续任务。

## 7. `src/api` 模块契约

前端页面只能调用 `src/api` 模块，不能直接调用 Supabase。

这样可以在 UI 开发阶段保持 mock 模式，后续再切换到真实后端。

### 当前 API 模式设计

`src/api/client.js` 负责 API 模式和共享响应工具。

当前函数：

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

环境变量：

```bash
EXPO_PUBLIC_API_MODE=mock
EXPO_PUBLIC_SUPABASE_URL=
EXPO_PUBLIC_SUPABASE_ANON_KEY=
EXPO_PUBLIC_APP_NAME=独家童话
```

统一成功响应结构：

```js
{
  success: true,
  data: {},
  meta: null,
  error: null,
}
```

统一错误响应结构：

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

## 8. 当前 API 模块

### `src/api/diaryApi.js`

用途：日记列表、详情、创建、更新、删除。

当前函数：

- `getDiaryList(params)`
- `getDiaryDetail(id)`
- `createDiary(payload)`
- `updateDiary(id, payload)`
- `deleteDiary(id)`

后续真实实现：

1. 读取当前用户 session。
2. 解析 active `couple_id`。
3. 查询或修改 `diaries` 表。
4. 返回标准化 diary 对象。

### `src/api/photoApi.js`

用途：照片上传和相册 API。

当前函数：

- `getPhotoTimeline(params)`
- `getAlbumList()`
- `uploadPhoto(payload)`
- `getAlbumDetail(albumId)`
- `deletePhoto(id)`

后续真实实现：

1. 通过 Expo ImagePicker 选择图片。
2. 上传文件到 Supabase Storage 的 `photos` bucket。
3. 向 `photos` 表插入记录。
4. 返回标准化 photo 对象。

### `src/api/anniversaryApi.js`

用途：纪念日列表、下一个纪念日、创建、更新、删除。

当前函数：

- `getAnniversaries()`
- `getAnniversaryList()` compatibility alias
- `getNextAnniversary()`
- `createAnniversary(payload)`
- `updateAnniversary(id, payload)`
- `deleteAnniversary(id)`

### `src/api/aiApi.js`

用途：AI 漫画和视频生成。

当前函数：

- `createComicJob(payload)`
- `createVideoJob(payload)`
- `getAiJobDetail(id)`
- `getAiCreationHistory()`
- `retryAiJob(id)`

后续真实实现：

1. 插入一条 `ai_jobs` 记录，状态为 `pending`。
2. 调用 Edge Function：`create-ai-comic-job` 或 `create-ai-video-job`。
3. Edge Function 校验用户和情侣访问权限。
4. Edge Function 调用外部 AI Provider。
5. Worker 更新任务状态和进度。
6. App 通过 `getAiJobDetail` 轮询，或通过 Realtime 监听。

### `src/api/coupleApi.js`

用途：情侣资料、邀请码、绑定和情侣时间线。

当前函数：

- `getCoupleInfo()`
- `getCurrentCouple()` compatibility alias
- `createInviteCode()`
- `bindCouple(inviteCode)`
- `bindCoupleByCode(code)` compatibility alias
- `updateCoupleInfo(payload)`
- `getCoupleTimeline()`

### `src/api/storageApi.js`

用途：图片和生成文件的存储抽象。

当前函数：

- `uploadImage(bucket, path, localUri, options)`
- `getSignedUrl(bucket, path, expiresIn)`
- `deleteFile(bucket, path)`

后续真实实现：

1. 上传二进制文件到 Supabase Storage。
2. 根据 bucket policy 返回 public URL 或 signed URL。
3. 删除记录时同步删除 Storage 对象。

## 9. Edge Functions

### `create-ai-comic-job`

输入：

- `sourceType`
- `sourceIds`
- `text`
- `style`
- `characterProfile`

输出：

- `jobId`
- `status`

职责：

- 校验用户 session。
- 校验情侣访问权限。
- 创建 AI job。
- 启动生成任务。
- 隐藏 AI Provider keys。

### `create-ai-video-job`

与漫画生成流程类似，但产出视频结果。

### `export-memory-pdf`

职责：

- 选择日记、照片和纪念日。
- 在服务端生成 PDF。
- 上传到 `exports` bucket。
- 返回签名下载 URL。

## 10. 开发阶段

### Phase 1：前端 Mock

- 当前 App 页面使用 mock 数据。
- API 模块返回 `requestMock`。
- 优先验证 UI 和流程。

### Phase 2：Supabase 集成

- 添加 Supabase project URL 和 anon key。
- 将 `requestMock` 替换为真实 Supabase 查询。
- 保持相同函数名，减少页面层改动。

### Phase 3：Storage 与 Auth

- 增加登录页。
- 增加 profile 表。
- 增加图片上传。
- 增加 RLS policies。

### Phase 4：AI Tasks

- 增加 Edge Functions。
- 增加 `ai_jobs` 表。
- 增加轮询或 Realtime 进度。
- 存储生成的漫画和视频。

### Phase 5：导出与备份

- PDF 导出。
- 数据备份。
- 存储空间管理。

## 11. 重要规则

- UI 页面不能知道数据库细节。
- 只有 `src/api` 可以和后端通信。
- AI keys 必须保留在服务端。
- Storage 路径必须包含 `couple_id`。
- 每张情侣数据表都必须包含 `couple_id`。
- 生产环境前必须开启 RLS。
- mock 响应结构应与真实响应结构保持一致。
- 引入真实模式后，mock 模式仍必须保持可用。

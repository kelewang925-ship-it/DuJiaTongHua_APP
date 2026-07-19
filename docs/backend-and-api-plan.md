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
- `type text`：`storyboard`、`comic`、`video`
- `job_kind text`：`storyboard`、`comicFromText`、`comicFromPhoto`、`videoFromText`、`videoFromImage`
- `source_type text`：`diary`、`photo`、`text`
- `source_ids text array`
- `style text`
- `character_profile jsonb`
- `prompt text`
- `provider text`
- `model text`
- `provider_request_id text`
- `config_version int`
- `access_tier text`：`free`、`vip`
- `input_config jsonb`：创建任务时的业务参数快照
- `billing_snapshot jsonb`：免费额度或点数成本、预扣和退款规则快照
- `status text`：`pending`、`processing`、`done`、`failed`、`cancelled`
- `progress int`
- `result_storage_paths text array`：只保存私有 Storage 对象路径
- `credits_reserved int`
- `credits_settled int`
- `billing_status text`：`reserved`、`settled`、`refunded`
- `error_message text`
- `error_code text`：返回 App 的稳定业务错误码
- `started_at timestamptz`
- `finished_at timestamptz`
- `created_at timestamptz`
- `updated_at timestamptz`

任务创建时必须快照配置版本、模型、权益、成本和运行参数。后续激活新配置不能改变在途任务的模型、扣点或退款逻辑。

### `ai_entitlements`

用户 AI 权益表。字段至少包括 `user_id`、`tier`、`source`、`starts_at`、`ends_at`、`is_test_grant` 和时间戳。第三阶段只使用有期限的测试 VIP 授权，不接真实支付。

### `ai_credit_wallets`

魔法点数钱包。字段至少包括 `user_id`、`balance`、`period_grant`、`rollover_amount`、`balance_cap`、`period_started_at`、`period_ends_at` 和 `updated_at`。客户端只读，所有变更通过受控 RPC/服务端事务执行。

### `ai_credit_ledger`

不可变点数流水。记录 `grant`、`reserve`、`settle`、`refund`、`adjustment`，并包含 `user_id`、`job_id`、`amount`、`balance_after`、`reason_code`、`idempotency_key` 和时间戳。禁止客户端更新或删除。

### `ai_daily_usage`

每日免费额度统计。按 `user_id + usage_date + capability` 唯一，记录 `used_count`、`reserved_count` 和 `config_version`。额度占用和任务创建必须在同一服务端事务内完成，防止并发超发。

### `ai_product_configs`

版本化 AI 产品配置。字段至少包括 `environment`、`version`、`status`、`config jsonb`、`created_by`、`created_at`、`activated_at`。状态为 `draft`、`active`、`retired`，每个环境只能有一个 active 版本。

第三阶段计划创建 draft `version = 1`；迁移和校验完成前 active 版本为无。v1 初始默认值：Free 每日 10 次分镜、每日 1 个漫画任务且每任务最多 4 张；VIP 每周期 60 点、最多结转 60 点、余额上限 120，默认每日 3 个免费漫画任务；低成本漫画 1 点/张、照片编辑 3 点/张、文生/图生视频 20 点/任务；视频每任务 1 段 720P；系统重试 1 次、App 轮询 5 秒、测试预算 ¥30/日。全部数量可通过后续配置版本调整。

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
ai-comics/{couple_id}/{user_id}/{job_id}/page-{index}.png
ai-videos/{couple_id}/{user_id}/{job_id}/result.mp4
exports/{couple_id}/{export_id}.pdf
```

`ai-comics`、`ai-videos` 必须保持私有。供应商返回临时 URL 后，服务端必须立即下载并持久化到对应 bucket；数据库只保存对象路径，App 通过服务端获取短期签名 URL。App 不得直接向 AI 结果 bucket 写入文件。

## 6. Auth 与安全规则

使用 Supabase Row Level Security。

规则：

- 用户只能读取自己的 profile。
- 用户只能读取自己 active couple 下的数据。
- 用户只能为自己的 active couple 创建日记和照片。
- 用户只能更新或删除自己创建的记录。
- AI 任务可由情侣双方任意一方创建。
- AI 任务创建必须由服务端原子校验功能开关、配置、权益、每日额度、点数和测试预算。
- App 不能直接写 `ai_entitlements`、钱包、流水、每日用量或产品配置。
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

第三阶段新增统一契约：

- `createAiJob(payload)`：统一创建分镜、漫画和视频任务；既有创建函数保留为兼容 wrapper。
- `getAiEntitlement()`：只读返回 tier、剩余免费额度、点数余额和到期时间。
- `getAiProductConfig()`：只返回 App 展示所需的公开配置摘要，不返回 provider、model 或内部价格。

第三阶段真实实现：

1. App 调用统一 Edge Function `create-ai-job`，只传 `jobKind`、素材、文本、风格、数量和 `clientRequestId`。
2. 客户端不能传 `provider`、`model`、`accessTier`、`creditCost` 或 `configVersion`。
3. Edge Function 校验 session、active couple、功能开关、每日预算和幂等键。
4. 服务端读取 active 配置，原子占用免费额度或预扣点数，并创建带配置/计费快照的 `pending` 任务。
5. Worker 调用供应商、更新状态、把临时结果写入私有 Storage，成功结算或技术失败退款。
6. App 默认每 5 秒通过 `getAiJobDetail` 轮询；后续可增加 Realtime，但返回结构保持一致。

创建响应至少返回 `jobId`、`status`、`configVersion`、本次额度/点数预扣摘要和最新只读权益摘要。错误使用稳定业务码，例如 `AI_DISABLED`、`VIP_REQUIRED`、`DAILY_QUOTA_EXCEEDED`、`INSUFFICIENT_CREDITS`、`TEST_BUDGET_EXCEEDED`、`PROVIDER_FAILED`、`STORAGE_PERSIST_FAILED`。

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

### `create-ai-job`

输入：

- `jobKind`
- `sourceType`
- `sourceIds`
- `text`
- `style`
- `characterProfile`
- `imageCount`
- `clientRequestId`

输出：

- `jobId`
- `status`
- `configVersion`
- `billing`
- `entitlement`

职责：

- 校验用户 session。
- 校验情侣访问权限。
- 校验 `AI_REAL_ENABLED` / `AI_VIP_ENABLED`、active 配置和测试预算。
- 原子占用每日额度或预扣魔法点数，并创建 AI job。
- 启动生成任务。
- 隐藏 AI Provider key、模型映射和内部价格。

### `process-ai-job`

职责：

- 按任务快照调用 SiliconFlow 对应模型。
- 最多执行配置指定的系统重试次数，v1 默认 1 次。
- 轮询或接收供应商任务状态。
- 把供应商临时结果立即持久化到私有 Storage。
- 成功时结算，技术失败时原子退款，并写入不可变点数流水。

服务端模型槽位初始映射：

```js
const AI_MODELS = {
  storyboard: 'Qwen/Qwen3.5-4B',
  comicFree: 'Kwai-Kolors/Kolors',
  comicEdit: 'Qwen/Qwen-Image-Edit-2509',
  comicCheap: 'Tongyi-MAI/Z-Image-Turbo',
  videoFromText: 'Wan-AI/Wan2.2-T2V-A14B',
  videoFromImage: 'Wan-AI/Wan2.2-I2V-A14B',
};
```

此映射存放在 `ai_product_configs.config`，不能放入 Expo 公共环境变量或由客户端选择。

### `export-memory-pdf`

职责：

- 选择日记、照片和纪念日。
- 在服务端生成 PDF。
- 上传到 `exports` bucket。
- 返回签名下载 URL。

## 10. 开发阶段

### 第一阶段：工程、界面与 Mock 基础（已完成）

- 当前 App 页面使用 mock 数据。
- API 模块返回 `requestMock`。
- 优先验证 UI 和流程。

### 第二阶段：Supabase 与核心业务真实化（当前 partial）

- 增加登录页。
- 增加 profile 表。
- 增加图片上传。
- 增加 RLS policies。
- 将 `requestMock` 替换为真实 Supabase 查询，同时保持相同函数名。
- 完成三账号 RLS/Storage 和双账号真实业务联调。

### 第三阶段：AI 真实化与权益系统（已规划、未实施）

- 增加版本化配置、功能开关、权益、魔法点数和每日额度。
- 扩展 `ai_jobs`，实现统一 Edge Function、供应商适配和任务快照。
- 完成私有 Storage 持久化、轮询、重试、结算和退款。
- 用测试授权验证 VIP，不接真实支付。
- 详细计划见 `docs/phase-3-ai-module-plan.md`。

### 后续阶段：支付、导出与上线

- 月卡 ¥18、年卡 ¥168 的真实订阅；不提供永久会员。
- PDF 导出。
- 数据备份。
- 存储空间管理。

## 11. 重要规则

- UI 页面不能知道数据库细节。
- 只有 `src/api` 可以和后端通信。
- AI keys 必须保留在服务端。
- AI provider、model、tier、成本和配置版本必须由服务端决定，客户端不得指定。
- 新配置只影响新任务，在途任务必须使用创建时的配置、模型和计费快照。
- 免费额度与点数占用、任务创建、结算和退款必须原子执行并可审计。
- Free 任务不能在失败时静默切换到高成本收费模型。
- 供应商临时结果必须立即转存私有 Storage，不能作为长期结果 URL。
- Storage 路径必须包含 `couple_id`。
- 每张情侣数据表都必须包含 `couple_id`。
- 生产环境前必须开启 RLS。
- mock 响应结构应与真实响应结构保持一致。
- 引入真实模式后，mock 模式仍必须保持可用。

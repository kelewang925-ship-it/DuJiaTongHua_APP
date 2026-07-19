# 《独家童话》第三阶段 AI 模块与权益系统计划

> 状态：已确定产品与技术方案，尚未开始真实联调。第三阶段必须在第二阶段 Supabase 基础能力和三账号权限验证完成后进入实施。

## 1. 阶段目标

第三阶段把现有 AI 页面从 mock 演示升级为可受控的真实生成能力，并在服务端建立 Free/VIP 权益、魔法点数、任务计费、失败退款和版本化配置。

本阶段交付：

- 文本/日记生成分镜与漫画。
- 照片编辑漫画、低成本漫画、文生视频和图生视频的 VIP 能力。
- 统一异步 AI 任务、进度查询、失败重试和历史记录。
- Free/VIP 服务端鉴权、每日免费额度、魔法点数钱包和流水。
- AI 结果持久化到私有 Supabase Storage。
- 可回滚、可审计的版本化服务端配置。
- 保留 mock 模式，便于无密钥开发和回归测试。

本阶段不交付：

- 真实支付、自动续费、退款和应用商店订阅。
- 后台管理 UI。
- 永久会员；产品只保留月卡 ¥18、年卡 ¥168，第三阶段通过测试授权模拟 VIP。
- 对生成质量作商业发布级承诺；第三阶段优先验证可调用、可计费、可追踪和可恢复。

## 2. 产品权益与初始默认值

以下数量均为首版默认值，必须由服务端配置表管理，不能硬编码到 App；后期可以创建新配置版本调整。

| 项目 | Free | VIP |
| --- | --- | --- |
| 分镜生成 | 每日 10 次 | 每日 10 次免费额度，可按配置扩展 |
| 文本/日记漫画 | 每日 1 个任务，每任务最多 4 张 | 默认每日 3 个免费任务；超额按点数结算 |
| 照片编辑漫画 | 不开放 | 3 点/张 |
| 低成本漫画 | 免费任务优先使用 | 1 点/张 |
| 文生视频 | 不开放 | 20 点/任务 |
| 图生视频 | 不开放 | 20 点/任务 |
| 视频规格 | 不开放 | 每任务 1 段 720P 视频 |
| 周期赠送点数 | 0 | 60 点/权益周期 |
| 结转规则 | 不适用 | 最多结转 60 点，余额上限 120 点 |

补充规则：

- 免费额度只能路由到免费/低成本模型，不能因供应商失败自动切到收费更高的模型。
- VIP 能力在第三阶段由服务端测试授权开启，不接真实支付。
- 技术失败且未产出有效结果时，服务端原子退还预扣点数或免费次数。
- 用户主动取消、违规输入、已经产出有效结果等场景是否退款由配置和错误码决定。
- 每个 AI 任务最多由系统自动重试 1 次；App 默认每 5 秒查询一次状态。
- 测试环境每日供应商预算默认 ¥30，达到预算后关闭新建真实任务，已创建任务继续按快照处理。

## 3. 服务端模型映射

首选供应商为 SiliconFlow。模型映射只存在于服务端配置，App 只能提交业务类型，不能提交供应商、模型、价格或权益等级。

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

业务 key 含义：

- `storyboard`：把日记或自由文本整理成漫画分镜、镜头描述和提示词。
- `comicFree`：Free 漫画任务使用的免费或活动模型槽位。
- `comicEdit`：基于用户照片做人物/画面编辑的高成本 VIP 模型槽位。
- `comicCheap`：文本漫画和低成本批量出图的模型槽位。
- `videoFromText`：根据文本和分镜生成视频。
- `videoFromImage`：根据图片或漫画画面生成视频。

模型是否可用及供应商实际价格可能变化。上线或切换配置前必须以供应商控制台实时验证为准，不能仅依赖本计划中的模型名。

## 4. 版本化配置协议

新增 `ai_product_configs` 表，使用 `draft -> active -> retired` 生命周期，同一环境只能存在一个 active 版本。

建议字段：

- `id uuid primary key`
- `environment text`：`development`、`staging`、`production`
- `version int`
- `status text`：`draft`、`active`、`retired`
- `config jsonb`
- `created_by uuid`
- `created_at timestamptz`
- `activated_at timestamptz`

初始计划版本为 `version = 1`；在迁移、校验和激活前，当前 active 版本必须记录为“无”。配置结构至少包括：

```json
{
  "models": {
    "storyboard": "Qwen/Qwen3.5-4B",
    "comicFree": "Kwai-Kolors/Kolors",
    "comicEdit": "Qwen/Qwen-Image-Edit-2509",
    "comicCheap": "Tongyi-MAI/Z-Image-Turbo",
    "videoFromText": "Wan-AI/Wan2.2-T2V-A14B",
    "videoFromImage": "Wan-AI/Wan2.2-I2V-A14B"
  },
  "free": {
    "storyboardPerDay": 10,
    "comicJobsPerDay": 1,
    "comicImagesPerJob": 4
  },
  "vip": {
    "comicJobsPerDay": 3,
    "periodCredits": 60,
    "rolloverCap": 60,
    "balanceCap": 120
  },
  "creditCosts": {
    "comicCheapPerImage": 1,
    "comicEditPerImage": 3,
    "videoFromTextPerJob": 20,
    "videoFromImagePerJob": 20
  },
  "runtime": {
    "systemRetryCount": 1,
    "pollIntervalSeconds": 5,
    "testDailyBudgetCny": 30,
    "videoResolution": "720p",
    "videoClipsPerJob": 1
  }
}
```

激活规则：

1. 新配置先写为 draft，并做 JSON Schema、模型槽位、非负数量、余额上限和成本校验。
2. 通过事务把旧 active 改为 retired，再激活新版本；数据库唯一约束保证每个环境只有一个 active。
3. 新配置只影响新任务。创建任务时把 `config_version`、模型、权益等级和预估成本快照写入 `ai_jobs`。
4. 在途任务永远按任务快照执行和退款，不能被后续配置修改改变。
5. 第三阶段不做管理后台，通过受控 SQL/服务端脚本创建和激活配置。

## 5. 数据模型

在既有 `ai_jobs` 上扩展，并新增：

- `ai_entitlements`：用户的 Free/VIP 类型、开始/结束时间、来源和测试授权标记。
- `ai_credit_wallets`：当前点数、周期赠送、结转和余额上限。
- `ai_credit_ledger`：赠送、预扣、结算、退款、人工调整的不可变流水。
- `ai_daily_usage`：按用户、日期和能力统计免费次数。
- `ai_product_configs`：版本化模型、额度、点数和运行参数。

数据库 RPC/服务端事务负责：

- 校验用户和 active couple。
- 读取 active 配置和权益。
- 原子占用每日额度或预扣点数。
- 创建带配置快照的任务。
- 成功结算或失败退款。

App 不得直接写钱包、流水、每日用量、权益或配置表。

## 6. API 与任务协议

统一创建入口：

```text
POST /functions/v1/create-ai-job
```

客户端允许提交：

- `jobKind`：`storyboard`、`comicFromText`、`comicFromPhoto`、`videoFromText`、`videoFromImage`
- `sourceType`、`sourceIds`
- `text`、`style`、`characterProfile`
- `imageCount` 或必要的业务参数
- `clientRequestId`：幂等键

客户端禁止提交：

- `provider`
- `model`
- `accessTier`
- `creditCost`
- `configVersion`

创建响应至少包含：

- `jobId`
- `status`
- `configVersion`
- `billing`：本次使用免费额度或预扣点数、预扣数量
- `entitlement`：剩余额度和点数的只读摘要

查询入口由 `getAiJobDetail(jobId)` 提供统一状态：`pending`、`processing`、`done`、`failed`、`cancelled`。供应商内部状态和错误信息必须映射为稳定的 App 错误码，不能把密钥、原始响应或敏感 prompt 返回客户端。

## 7. 任务、Storage 与安全流程

1. App 调用 `src/api/aiApi.js` 创建任务。
2. Edge Function 验证 session、情侣关系、功能开关、测试预算和幂等键。
3. 服务端读取 active 配置，选择模型，原子占用额度/点数并创建任务快照。
4. Worker 调用供应商；第三阶段默认允许 1 次系统重试。
5. 供应商返回临时 URL 后，服务端立即下载并写入私有 Storage：
   - `ai-comics/{couple_id}/{user_id}/{job_id}/page-{index}.png`
   - `ai-videos/{couple_id}/{user_id}/{job_id}/result.mp4`
6. `ai_jobs` 只保存 Storage 对象路径，不把供应商临时 URL 作为长期结果。
7. App 通过服务端获取短期签名 URL 展示；RLS/Storage policy 限制为 active couple 成员。
8. 成功时结算；技术失败时按任务快照原子退款，并记录 ledger 和稳定错误码。

所有 SiliconFlow key 只保存在 Supabase Edge Function secret 中；不得写入 Expo 环境变量、仓库、日志或客户端请求。

## 8. 功能开关与环境

第三阶段至少提供：

- `AI_REAL_ENABLED`：是否允许创建真实供应商任务，初始为 `false`。
- `AI_VIP_ENABLED`：是否开放 VIP 能力，初始为 `false`。
- `SILICONFLOW_API_KEY`：仅服务端 secret，不记录值。

数量、模型、成本、重试和预算放在版本化配置表；功能开关负责紧急启停。关闭真实模式时，App 应继续支持 mock 演示，不能静默调用真实供应商。

## 9. 测试账号与联调矩阵

测试账号不在文档中保存密码或 token。进入第三阶段前准备：

- 账号 A、B：已绑定的 active couple，用于跨账号任务可见性和 Storage 权限验证。
- 账号 C：未绑定或非该 couple 成员，用于 RLS、任务查询和签名 URL 越权测试。
- VIP 测试授权：为 A 或 B 写入有期限的测试 entitlement，验证点数预扣、结算、退款和到期降级。

核心用例：

- Free 分镜和漫画额度边界、跨日归零、并发请求不超发。
- Free 不能创建照片编辑或视频任务。
- VIP 点数不足、并发预扣、成功结算、技术失败退款。
- 配置切换后旧任务保持旧版本快照，新任务使用新版本。
- 供应商超时、限流、临时 URL 失效、Storage 写入失败和一次重试。
- 预算达到 ¥30 后拒绝新真实任务，但 mock 模式和历史查询可用。

## 10. 实施批次与验收

### 3.1 数据与配置基础

- 增加迁移、约束、RLS、私有 buckets 和原子 RPC。
- 写入并验证 draft v1；完成测试后才激活。

### 3.2 服务端任务闭环

- 实现统一创建、供应商适配器、轮询/回调、重试、Storage 持久化和退款。
- 先打通 `storyboard` 与 `comicCheap`，再接照片编辑和视频。

### 3.3 App 接线

- 保持现有页面结构，统一接入 `src/api/aiApi.js`。
- 展示权益摘要、预估扣点、稳定进度、失败原因和重试入口。
- 保持 mock/real 返回结构一致。

### 3.4 安全与成本验收

- 三账号 RLS/Storage 越权测试通过。
- 日额度和点数在并发下不超发、不重复扣除。
- 生成文件已经落入私有 Storage，历史记录不依赖供应商临时 URL。
- 仓库和 App bundle 不包含供应商 key、服务端模型选择或内部价格。
- 达到测试预算后可自动熔断，并能通过功能开关立即停止新任务。

第三阶段只有在上述验收完成、真实任务至少覆盖一个 Free 漫画闭环和一个 VIP 点数闭环后，才能标记为完成。

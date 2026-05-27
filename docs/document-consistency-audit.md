# 《独家童话》文档一致性整理记录

> 文档说明：本文档用于记录《独家童话》文档体系的一致性整理结果，包括标题风格、文档说明格式、Phase/阶段命名、mock MVP/真实能力定义、文件结构覆盖度和待补页面计划一致性检查。

---

## 1. 本次整理目标

本次整理重点不是翻译，而是统一文档体系中的表达方式和索引关系。

整理目标：

1. 统一文档标题风格。
2. 统一“文档说明”格式。
3. 统一 `Phase` / `阶段` 命名。
4. 统一 `mock MVP` / `真实能力` 的描述。
5. 检查 `docs/project-file-structure.md` 是否包含所有最新页面和文档。
6. 检查 `docs/pending-interfaces-implementation-plan.md` 是否与当前 `app/` 路由一致。

---

## 2. 文档标题风格

当前推荐标题格式：

```text
# 《独家童话》xxx
```

适用范围：

- 产品计划文档；
- 设计文档；
- 接手提示词；
- 页面实现计划；
- 图片资产计划；
- 测试验收提示词。

允许保留英文/技术名词的情况：

- `Design System`
- `Codex`
- `Supabase`
- `API`
- `mock MVP`
- `Phase`
- 文件路径、函数名、表名、环境变量、命令。

---

## 3. 文档说明格式

当前统一格式：

```markdown
# 文档标题

> 文档说明：本文档用于……
```

已经适配该格式或具备等价说明的文档包括：

- `docs/project-file-structure.md`
- `docs/pending-interfaces-implementation-plan.md`
- `docs/image-assets-guideline.md`
- `docs/image-assets-implementation-plan.md`
- `docs/next-chat-handoff-prompt.md`
- `docs/codex-page-acceptance-test-prompt.md`
- `docs/visual-audit-and-next-steps.md`
- `docs/app-development-guide.md`
- `docs/design-system-v1.md`
- `docs/backend-and-api-plan.md`
- `docs/interface-architecture-design.md`
- `docs/interface-list.md`
- `docs/supabase-auth-setup.md`

后续新增文档必须使用该格式。

---

## 4. `Phase` / `阶段` 命名规则

统一规则：

| 场景 | 推荐写法 |
| --- | --- |
| 路线图标题 | `Phase 5：Supabase 接入阶段` |
| 正文说明 | “当前处于 Supabase 接入阶段” |
| 任务编号 | `任务 5.1` / `Phase 5.1` 均可，但同一文档内保持一致。 |
| 提交说明 | 可保留 `phase-x: 简短说明`，便于 Codex 和 Git 记录。 |

原则：

- 路线图可以保留 `Phase`，因为它便于开发阶段编号。
- 中文正文优先使用“阶段”。
- 不再混用“阶段 / Phase / 版本 / 批次”表达同一个概念。

---

## 5. `mock MVP` / `真实能力` 描述规则

统一定义：

| 术语 | 含义 |
| --- | --- |
| `mock MVP` | 不接真实后端、不接真实 AI、不接真实文件服务，仅用本地 state/mock 数据完成可演示交互闭环。 |
| `真实能力` | 需要接入 Supabase、Storage、真实 AI、PDF 导出、系统相册、登录态、真实上传/下载等生产能力。 |
| `骨架页` | 只有说明或静态展示，没有状态和交互闭环的页面。当前 `app/` 路由中骨架页数量为 0。 |
| `兼容路由` | 为旧入口、历史设计稿或跳转兼容保留的转发页面，不作为新的主开发入口。 |

文档使用要求：

- 已具备本地交互的页面统一标记为 `mock MVP`。
- 不要把 mock MVP 写成“真实完成”。
- 未接真实服务的能力必须明确标记为“真实能力待接入”。

---

## 6. `project-file-structure.md` 检查结果

本次已将 `docs/project-file-structure.md` 重整为当前项目索引版。

已补齐内容：

- 全局、引导、登录、设置、草稿、搜索、帮助、空状态、分享、会员页面；
- 四个主 Tab 页面；
- 账号与情侣关联页面；
- 日记、标签、时光胶囊页面；
- 照片与相册页面；
- AI 配置、进度、结果、人设、历史页面；
- 情侣互动、评论、通知、兼容路由；
- 纪念日管理、倒计时、编辑、模板页面；
- 数据备份、PDF 配置、导出预览、存储管理页面；
- `src/components/` 组件清单；
- `src/theme/`、`src/store/`、`src/data/`、`src/api/`、`src/screens/`；
- `supabase/` 文件；
- `assets/design/` 和 `assets/images/`；
- 当前 `docs/` 文档清单；
- 当前关键业务闭环。

检查结论：

```text
project-file-structure.md 已覆盖当前主要页面、组件、状态、API、文档和资产目录。
```

---

## 7. `pending-interfaces-implementation-plan.md` 检查结果

本次已为 `docs/pending-interfaces-implementation-plan.md` 增加“术语统一”区。

当前结论：

```text
当前 app/ 路由中 FeaturePage 骨架页数量：0
未落地主页面/子页面数量：0（以当前路由清单为准）
```

已经完成的 P1 页面：

- 互动通知页：`app/notifications/index.js`
- 标签管理页：`app/tags/index.js`
- 时光胶囊设置页：`app/time-capsule/settings.js`
- 导出预览页：`app/data/export-preview.js`
- 存储空间管理页：`app/data/storage.js`

连续推进记录中也已覆盖：

- 纪念日添加/编辑独立页；
- 纪念日专属记录模板页；
- AI 漫画结果详情页；
- AI 人设管理页；
- 分享预览页；
- 会员权益说明页；
- FairyImage 渲染通道；
- Zustand persist；
- 历史骨架路由重定向；
- 账号链路页面；
- 辅助页面。

检查结论：

```text
pending-interfaces-implementation-plan.md 与当前 app 路由状态基本一致。
```

---

## 8. 当前仍需后续关注的真实能力

虽然路由和 mock MVP 页面已经基本覆盖，但以下内容仍属于真实能力待接入：

1. 真实 Supabase 数据 CRUD；
2. 真实 Storage 图片/视频/PDF 上传；
3. 真实 AI 漫画/视频生成；
4. 真实 PDF 文件导出；
5. 系统相册 ImagePicker；
6. 完整登录态启动判断和情侣绑定状态判断；
7. 真实图片资源首批替换；
8. 自动化测试和端到端验证。

---

## 9. 后续维护规则

1. 新增文档必须使用：`# 标题` + `> 文档说明：...`。
2. 新增页面必须更新 `docs/project-file-structure.md`。
3. 新增待办或完成页面必须更新 `docs/pending-interfaces-implementation-plan.md`。
4. 新增图片资产必须更新 `docs/image-assets-guideline.md`。
5. 新增真实能力接入必须同步更新相关运行手册和后端/API 文档。
6. 不要把 mock MVP 写成真实生产完成。
7. 不要将设计图整图直接作为页面图片使用。

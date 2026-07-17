# 《独家童话》Android 视觉对齐清单

更新时间：2026-07-14

## 验收基线

- 最终平台：Android，目标原始截图 1440 × 3168 px，系统字体标准（fontScale = 1）。
- 当前设备状态：已找到 `D:\Program Files\HBuilderX\plugins\launcher-tools\tools\adbs\adb.exe`，但 `adb devices -l` 为空；本轮无法读取逻辑尺寸、density、系统栏 insets 或原始截图。
- Web 只用于构建和布局冒烟检查，不作为视觉完成依据。
- Git 起始状态：`main...origin/main`，工作区干净。
- dev-ui-lab：路由存在，但默认由 `enableDevUI` 控制；关闭时会重定向，不能直接作为 Android 验收替代。

## 分类说明

- 黄金基准页面：用户明确确认已对齐，禁止主动改动。
- 部分实现：有独立页面结构和静态交互，但尚未完成本轮 Android 截图对比。
- 视觉差异较大：实现与效果图的主要构图明显不一致。
- 只有占位内容：通用说明页、mock 预览或明确占位文案。
- 尚未实现：设计稿存在但没有对应可打开路由。
- 已基本对齐：需要 Android 截图证据；本轮设备离线，因此不新增该标记。

## 效果图—路由—实现文件映射

| 效果图 | 路由 | 实现文件 | 当前状态 | 备注 |
| --- | --- | --- | --- | --- |
| 引导页.png | `/onboarding` | `app/onboarding.js` | 黄金基准页面 | 受保护 |
| 登录页.png | `/login` | `app/login.js` | 黄金基准页面 | 受保护 |
| 情侣邀请页.png / v2 | `/account/invite` | `app/account/invite.js` | 黄金基准页面 | 受保护 |
| 情侣绑定确认页.png | `/account/bind-confirm` | `app/account/bind-confirm.js` | 黄金基准页面 | 受保护 |
| 情侣信息设置页.png | `/account/couple-info` | `app/account/couple-info.js` | 黄金基准页面 | 受保护 |
| 日记详情页.png | `/diary/detail` | `app/diary/detail.js` | 黄金基准页面 | 受保护、当前默认入口 |
| 02-首页-记录中心.png | `/(tabs)` | `app/(tabs)/index.js` | 代码/构建完成，Chrome 待复验 | `FairyPage` 根 + `tabSafe`；主 Tab 按设计保留沉浸式内容题名、不显示标准 FairyHeader；动态日期、响应式 Hero/统计/快捷入口、最近记录和 MemoryWall 完成；Web/Android export、4 Tab HTTP 与静态检查通过 |
| 03-情侣空间.png | `/(tabs)/couple` | `app/(tabs)/couple.js` | 代码/构建完成，Chrome 待复验 | `FairyPage` 根 + `tabSafe`；主 Tab 按设计不显示标准 FairyHeader；响应式双人主视觉、统计、想你/纪念日/时光胶囊/留言入口、预览和时间线完成；Web/Android export、HTTP 与静态检查通过 |
| 04-AI童话工坊.png | `/(tabs)/workshop` | `app/(tabs)/workshop.js` | 代码/构建完成，Chrome 待复验 | `FairyPage` 根 + `tabSafe`；主 Tab 按设计不显示标准 FairyHeader；响应式正式 Hero、草稿箱、四类 AI 入口、最近作品与创作历史完成；Web/Android export、HTTP 与静态检查通过 |
| 08-更多功能.png | `/(tabs)/mine` | `app/(tabs)/mine.js` | 代码/构建完成，Chrome 待复验 | `FairyPage` 根 + `tabSafe`；主 Tab 按设计不显示标准 FairyHeader；响应式资料/统计、会员入口、管理目录和退出确认完成；Web/Android export、HTTP 与静态检查通过 |
| 日记编辑器.png | `/diary/editor` | `app/diary/editor.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；富文本自动保存、可操作草稿、心情/标签、真实图片附件、保存与响应式纸页完成；Web/Android export、HTTP 与静态检查通过，语音/位置待原生服务阶段 |
| 照片上传页.png | `/photo/upload` | `app/photo/upload.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；真实系统相册多选、1–9 张预览/移除、表单校验、标签和持久化保存完成；Web/Android export、HTTP 与静态检查通过 |
| 相册浏览页.png | `/photo/album` | `app/photo/album.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；真实首图/正式素材回退、网格/时间线、筛选、展开与删除完成；Web/Android export、HTTP 与静态检查通过 |
| 时光胶囊设置页.png | `/time-capsule/settings` | `app/time-capsule/settings.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；未来日期/内容校验、多类封存、提醒、持久化列表、删除与隐私锁定完成；Web/Android export、HTTP 与静态检查通过 |
| 标签管理页.png | `/tags` | `app/tags/index.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；4 类标签册、持久化新增/编辑/删除、使用次数、记录筛选与反馈完成；Web/Android export、HTTP 与静态检查通过 |
| 情侣动态详情页.png | `/couple/activity-detail` | `app/couple/activity-detail.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；故事纸页、正式回忆主视觉、喜欢/收藏/评论、伴侣回应和后续创作入口完成；Web/Android export、HTTP 路由与静态检查通过 |
| 评论列表页.png | `/comments` | `app/comments/index.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；回忆上下文、评论/回复/喜欢、私密提示、计数和发送反馈完成；Web/Android export、HTTP 路由与静态检查通过 |
| 互动通知页.png | `/notifications` | `app/notifications/index.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；全部已读、分类筛选、未读状态、路由跳转和空筛选完成；Web/Android export、HTTP 路由与静态检查通过 |
| AI漫画生成配置页.png | `/ai/comic-config` | `app/ai/comic-config.js` | 当前阶段完成 | 素材、画风、分镜、隐私与画质配置及生成跳转完成；Chrome 360/1200 宽度与 Web 构建已通过，Android 原生效果待人工验证 |
| 文本转漫画页.png | `/ai/text-to-comic` | `app/ai/text-to-comic.js` | 当前阶段完成 | 日记富文本清理、自由输入、画风、分镜、正式预览素材与生成跳转完成；Chrome 360/1200 宽度与 Web 构建已通过，Android 原生效果待人工验证 |
| 照片转漫画页.png | `/ai/photo-to-comic` | `app/ai/photo-to-comic.js` | 当前阶段完成 | 正式照片素材选择、画风、氛围、细节、漫画预览与生成跳转完成；Chrome 360/1200 宽度与 Web 构建已通过，Android 原生效果待人工验证 |
| AI短视频配置页.png | `/ai/video-config` | `app/ai/video-config.js` | 当前阶段完成 | 回忆来源、视频风格、时长、字幕音乐、封面与生成跳转完成；Chrome 360/1200 宽度与 Web 构建已通过，Android 原生效果待人工验证 |
| 视频预览编辑页.png | `/ai/video-preview` | `app/ai/video-preview.js` | 当前阶段完成 | 正式主视觉、封面/字幕/音乐/片段编辑与保存分享反馈完成；复用 FairyPage、FairyHeader、FairyCard、FairyImage、FairyInput、FairyButton、FairyToast；Web 构建、Android bundle/export 与 Chrome 1912×956 交互已通过，Android 原生效果待人工验证 |
| 生成进度页.png | `/ai/progress` | `app/ai/progress.js` | 当前阶段完成 | 绘本进度、步骤状态、后台等待、历史与漫画/视频结果路由完成；Web 构建已通过，Android 原生效果待人工验证 |
| 创作历史展示页.png | `/ai/history` | `app/ai/history.js` | 当前阶段完成 | 分类筛选、作品卡、进度、完成态路由、分享反馈与空状态完成；复用 FairyPage、FairyHeader、FairyCard、FairyImage、FairyTag、FairyEmptyState、FairyToast；Web 构建、Android bundle/export 与 Chrome 筛选/分享/进度跳转已通过，Android 原生效果待人工验证 |
| 06-纪念日管理.png | `/anniversary` | `app/anniversary/index.js` | 代码/构建完成，Chrome 待复验 | 响应式纪念册总览、分类筛选、列表编辑、空分类和倒计时入口完成；Web/Android export、HTTP 路由与静态检查通过，Chrome Extension 缺失待实时复验 |
| 纪念日添加编辑页.png | `/anniversary/edit` | `app/anniversary/edit.js` | 代码/构建完成，Chrome 待复验 | 新增/编辑保存、日期校验、类型、年度重复、提醒、封面色和备注完成；Web/Android export、HTTP 路由与静态检查通过，Chrome Extension 缺失待实时复验 |
| 纪念日倒计时页.png | `/anniversary/countdown` | `app/anniversary/countdown.js` | 当前阶段完成 | 纪念日切换、提醒开关和路由交互完成；Web 构建已通过，Android 原生效果待人工验证 |
| 纪念日专属记录模板页.png | `/anniversary/template` | `app/anniversary/template.js` | 代码/构建完成，Chrome 待复验 | 5 套响应式模板、正式封面缩略图、选中态、问题预览、帮助反馈和带预设编辑跳转完成；Web/Android export、HTTP 路由与静态检查通过，Chrome Extension 缺失待实时复验 |
| PDF导出配置页.png | `/data/pdf-export` | `app/data/pdf-export.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；范围、内容、5 套正式封面、纸张、清晰度和参数化预览跳转完成；Web/Android export、HTTP 路由与静态检查通过 |
| 导出预览页.png | `/data/export-preview` | `app/data/export-preview.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；4 类页缩略图、动态目录/页数/体积、返回修改、分享和导出状态完成；Web/Android export、HTTP 路由与静态检查通过 |
| 数据备份恢复页.png | `/data/backup` | `app/data/backup.js` | 当前阶段完成 | 备份/恢复模拟、自动备份、频率、空间和历史记录完成；Web 构建已通过，Android 原生效果待人工验证 |
| 存储空间管理页.png | `/data/storage` | `app/data/storage.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；正式绘本主视觉、空间占用/图例、分类选择、缓存安全清理和会员入口完成；Web/Android export、HTTP 路由与静态检查通过 |
| 搜索页.png | `/search` | `app/search.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；热门/最近搜索、跨 4 类业务数据检索、5 类筛选、响应式结果卡和路由完成；Web/Android export、HTTP 与静态检查通过 |
| 草稿箱.png | `/drafts` | `app/drafts.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；筛选、继续编辑、单项删除、批量清理、确认与反馈完成；Web/Android export、HTTP 与静态检查通过 |
| 分享预览页.png | `/share-preview` | `app/share-preview.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；4 种正式风格、隐私控制、保存反馈、系统分享与响应式预览完成；Web/Android export、HTTP 与静态检查通过 |
| 会员权益说明页.png | `/membership` | `app/membership.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；正式主视觉、5 类权益、3 档方案、协议门槛、确认和本地体验成功态完成；Web/Android export、HTTP 与静态检查通过 |
| 帮助与反馈页.png | `/help-feedback` | `app/help-feedback.js` | 代码/构建完成，Chrome 待复验 | 标准 `FairyPage.header + FairyHeader` 骨架；正式信箱视觉、5 项 FAQ、3 类反馈、校验、本地受理编号和回执完成；Web/Android export、HTTP 与静态检查通过，截图上传待服务阶段 |
| 设置页.png | `/settings` | `app/settings.js` | 当前阶段完成 | 分组设置、开关、主题选择、数据入口和退出确认完成；Web 构建已通过，Android 原生效果待人工验证 |
| 空状态页.png | `/empty-state` | `app/empty-state.js` | 当前阶段完成 | 响应式绘本空状态，Web 构建已通过；Android 原生效果待人工验证 |

## 无独立效果图或别名路由

- `/account/couple-settings`：通用 `FeaturePage` 占位；索引没有同名独立效果图，疑似旧入口。
- `/ai/comic-result`：当前阶段完成；索引没有对应成功页效果图，已按 AI 模块设计体系补齐三联绘本结果、分镜切换、收藏、保存、分享和重新生成入口。
- `/records/tags`、`/records/time-capsule`、`/interaction/notifications`：兼容别名，分别重定向到正式路由。
- `/album` 与 `/photo/album`、`/interaction/comments` 与 `/comments`：存在重复业务入口，后续应以效果图对应的正式路由为验收对象。
- 八张总览图中的 `01-账号与关联`、`05-AI创作流程`、`07-数据与导出` 是模块总览，不强制映射为单一业务页。

## 第一批优先级

1. 继续从“部分实现”页面中选择结构和交互缺口较大的页面，优先完成同一业务模块。

## 2026-07-14 阶段 0 与首批进度

- 稳定开发基线见 `docs/stable-development-baseline.md`。
- `/album`、`/interaction/comments`、`/ai/generation-progress` 已改为正式路由兼容重定向。
- `src/assets/fairyImages.js` 已成为正式图片单一注册表，`FairyImage` 不再维护重复路径表。
- `/empty-state` 已完成响应式收尾：保留效果图构图和交互，使用正式 `empty-diary-v1.png` 复杂插画，移除整页坐标缩放与禁止字体缩放。
- `/anniversary/countdown` 已完成绘本倒计时卡片、纪念日切换、提醒开关、详情/模板/分享跳转，并复用正式 `anniversaryCover` 插画。
- `/data/backup` 已完成备份进行态、成功提示、恢复确认、自动备份、频率选择、空间占用和历史记录，并复用正式 `exportCover` 插画。
- `/settings` 已完成账号/关系、提醒/隐私、外观/存储和支持分组，补齐开关、主题选择、正确路由和退出确认。
- `/ai/comic-result` 已移除编号方块和 mock 占位文案，接入生成的三联绘本漫画，补齐分镜说明、收藏、保存、分享和重新生成入口。
- `/ai/progress` 已补齐绘本生成视觉、步骤状态和后台等待说明，生成完成后按漫画/视频类型进入正确结果页。
- 首个 6 页阶段的 Android 人工验证清单见 `docs/android-validation-stage-1.md`。
- `npm run check:web` 已通过。2026-07-16 已使用 Chrome 对 `/ai/text-to-comic`、`/ai/comic-config` 及其 `/ai/progress` 生成跳转完成实时验证：360×800 与 1200×900 均无横向溢出，正式图片加载成功，控制台 error 0；存在 React Native Web `shadow*` 弃用 warning。Android 与 iOS 设备级视觉均未执行。
- 2026-07-16 已继续完成 `/ai/photo-to-comic` 与 `/ai/video-config`：复用现有正式绘本图片，没有新增复杂素材；Chrome 交互、生成元数据、360×800 与 1200×900 无横向溢出验证通过，控制台 error 0；本批 Web 导出、diff 检查与跨平台 API 扫描通过。
- 2026-07-16 已继续完成 `/ai/video-preview` 与 `/ai/history`：视频预览的封面、字幕、音乐、保存反馈，以及历史页的视频/生成中筛选、分享反馈、进度跳转均完成 Chrome 实时验证，控制台 error 0；两页随后完成 `@/*` → `src/*` 路径别名试点，Web 与 Android bundle/export 级检查通过。

## 公共组件与重复模式

- 当前 AI 批次主要复用 `FairyPage`、`FairyHeader`、`FairyCard`、`FairyImage`、`FairyInput`、`FairyButton`、`FairyTag`、`FairyEmptyState`、`FairyToast` 与主题 spacing/colors token。
- 本批没有修改高使用率公共组件，也没有新增职责重复的组件，因此不需要扩大到既有页面和受保护页面回归。
- “区块标题 + 右侧说明”“图片选择卡”已在多个 AI 页面重复出现，但不同页面的图标、尺寸、卡片密度和交互语义差异仍较大；当前保留页面级实现，后续若第三种稳定同构用法出现，再评估提取向后兼容的模块组件。

## 共享组件风险

- `FairyPage` 负责移动端顶部 safe-area、滚动头部模糊与阴影；修改会影响大量页面和黄金基准页。
- `FairyButton`、`FairyCard` 被黄金页面复用；第一批页面使用页面级样式，不修改共享默认视觉。
- `FairyTabBar` 已在首页批次向后兼容接入移动端 `insets.bottom`，Web 维持 0；Android/iOS 实际系统栏高度和手势区仍须真机确认。

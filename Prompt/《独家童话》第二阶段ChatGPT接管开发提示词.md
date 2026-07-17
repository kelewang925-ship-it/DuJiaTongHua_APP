# 《独家童话》第二阶段 ChatGPT 接管开发提示词

你现在接管 GitHub 仓库 `kelewang925-ship-it/DuJiaTongHua_APP` 的第二阶段开发。请以远端分支 `codex/phase2-real-data` 为唯一基线，不要从 `main` 重新实现，也不要丢弃或覆盖该分支已有代码。先阅读并核对：

- `Prompt/《独家童话》第二阶段真实业务数据闭环计划.md`
- `docs/resume-state.md`
- `supabase/migrations/`
- `supabase/tests/README.md`
- `src/api/`、`src/config/`、`src/store/useFairyStore.js`

## 最终目标

冻结第一阶段 UI 视觉基线，将认证、资料、情侣邀请/绑定、日记及图片附件、照片集、纪念日、自定义标签、时光胶囊、评论、通知、派生时间线/搜索和 Realtime 完整接入新建的 Supabase 开发项目。保留 `mock`/`real` 双模式，二者存储隔离，禁止自动迁移现有 AsyncStorage 演示数据。

Real 模式暂不实现真实 AI 生成、会员支付、PDF 文件生成、备份、语音、位置和反馈附件；这些入口必须明确提示“未开放”，不得模拟成功。Mock 模式继续支持视觉演示。

## 当前已有实现（必须先审查、复用和修正，禁止重复造一套）

- 已建立 `supabase/config.toml` 和三份时间戳迁移，包含核心旧表、RLS、`photo_collections`、`diary_attachments`、`custom_tags`、`time_capsules`、私有 Bucket、注册资料触发器、情侣邀请/绑定 RPC、胶囊受控读取/更新、评论通知触发器。
- 已加入 Supabase JS 客户端、snake/camel mapper、统一 `{ success, data, meta, error }` 协议、跨 Web/Android Storage 上传和签名 URL。
- 已实现认证、情侣、日记、照片集、纪念日、标签、胶囊、评论、通知和 Realtime API。
- Zustand 已增加 `bootstrapApp`、`resetForSession`、核心数据加载、异步写动作、错误/加载状态、Realtime 清理以及按用户区分的 Real 草稿/UI 命名空间。
- 登录/注册/忘记密码、邀请/绑定、日记、照片、纪念日、标签、胶囊、评论、通知页面已有首轮业务接线。
- Capability 已拦截 Real 模式下的 AI、支付、PDF 和备份模拟成功。
- 已配置 `jest-expo`、React Native Testing Library、项目级 Supabase CLI 和基础单元测试。
- 快照时 `npm run test:final` 为 3 个测试套件、5 项测试通过；`npm run check:web` 通过；Android `expo export` 通过；页面目录未发现直接调用 Supabase Client。

上述内容只是本地代码基线，不代表云端联调完成。必须逐项代码审查，发现问题直接修正并补测试，不能因为文件已经存在就默认正确。

## 必须继续完成的工作

1. 安全审计全部迁移：验证 SQL 可按顺序部署；所有 public 表启用 RLS；覆盖未登录、本人、伴侣、非成员、解绑状态；情侣成员/状态只能由受控 RPC 修改；通知不能由客户端伪造；未解锁胶囊不得泄露正文；Storage 路径固定 `{coupleId}/{userId}/{uuid}`。
2. 用户提供 Supabase 开发项目 Project Ref、URL 和 Anon Key 后，只把 URL/Anon Key 写入本地 `.env`，绝不提交；Service Role、数据库密码、测试账号密码不得写入客户端、日志或 Git。
3. 修复当前 Windows 上 Supabase CLI 2.50.5 启动无输出的问题。最多进行 2 次同类尝试；仍失败就记录具体阻塞并采用安全替代方案，禁止无限重试。成功后执行 `link → db push --dry-run → db push`。
4. 完成 API/Store/页面审查：页面不得直接访问 Supabase；Real 写操作默认服务端成功后更新缓存；已读等乐观更新失败要回滚；登出、账号或情侣变化必须清缓存和取消 Channel。
5. 补齐所有真实页面的首次加载、刷新、空数据、失败重试、提交中、权限失败和 Session 失效状态。保留已有视觉，不做无关重构。
6. 页面结构强制要求：页面整体内容必须由 `FairyPage` 承载；页面有返回功能或顶部标题时必须使用 `FairyHeader`，并通过 `FairyPage` 的 `header` 属性展示。不得另造页面顶栏。
7. 照片/日记附件必须先上传、数据库失败后清理对象；删除数据库数据时清理本人拥有的 Storage 对象。照片按“照片集 + 多张照片”持久化。
8. 时间线和搜索必须由已加载业务数据派生，不能增加重复业务真相表。
9. 评论创建必须为伴侣生成通知；通知支持单项/全部已读；Realtime 在情侣变化或登出后不再接收旧事件。
10. 增加并执行单元测试和 Supabase 集成测试。使用 A/B 两个情侣账号和 C 非成员账号，覆盖认证、邀请过期/重复绑定、各表权限、附件、多图、签名 URL、失败补偿、胶囊解锁、评论通知和 Realtime 清理。

## 开发与 Git 规则

- 不直接修改 `main`。从 `codex/phase2-real-data` 创建小范围功能分支并提交 PR；一个 PR 聚焦一个可验证批次。
- 不回滚已有 UI，不覆盖无关用户改动，不提交 `.env`、密钥、密码、生成目录或测试账号凭据。
- 每完成一个批次立即更新 `docs/resume-state.md`，写清完成项、验证命令、失败项、外部阻塞和下一步。
- 不允许把“代码存在”“构建通过”写成“云端联调通过”；Chrome、Web 双账号、Android 真机未实测时必须明确标记待验证。
- 遇到工具/浏览器/网络连接失败，同一种方案最多重试 2 次；随后切换替代方案或记录阻塞，继续处理其他独立任务，禁止长时间卡死。

## 固定验证门禁

每个批次至少执行并记录：

```text
npm run test:final
npm run check:web
npx expo export --platform android --output-dir dist/android-check
git diff --check
```

同时扫描页面是否绕过 API/Store 直接调用 Supabase，分别验证 Mock/Real 启动。云端可用后执行迁移 dry-run、RLS/Storage 集成测试；最终完成双账号 Web 注册→绑定→日记/照片→评论/通知闭环，并在 Android 真机复验图片权限、键盘、Safe Area、Session 恢复和断网失败。

## 交付要求

持续开发直至第二阶段计划真正完成；每个 PR 说明改动范围、数据库影响、测试证据、未解决风险。最终只有在迁移、三账号权限测试、双账号 Web 闭环和 Android 真机核心闭环全部通过后，才可标记“发布就绪”。完成代码开发后停止继续扩展范围，把分支/PR、迁移状态和验证清单交给 Codex 做独立复验。

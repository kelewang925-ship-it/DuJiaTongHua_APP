# 《独家童话》开发运行手册

> 更新时间：2026-05-26
> 适用范围：Expo React Native / Expo Router / Supabase 接入阶段

本文档用于帮助新开发者拉取项目后完成安装、启动、调试和基础问题排查。当前项目支持 mock 模式和 Supabase real 模式。

---

## 1. 环境要求

推荐环境：

- Node.js：24.3.0
- npm：随 Node 24.3.0 安装的 npm 版本
- Expo CLI：使用项目本地依赖，不需要全局安装
- Git
- Expo Go：用于真机扫码调试
- Supabase 项目：仅 real 模式需要

Windows + nvmd 环境建议先确认 Node 版本：

```bash
node -v
npm -v
```

如果提示默认 Node 版本未设置，先在本机执行：

```bash
nvmd use 24.3.0
```

如果当前终端仍未生效，关闭终端后重新打开，再执行 `node -v`。

---

## 2. 安装依赖

首次拉取项目后，在项目根目录执行：

```bash
npm install
```

Phase 5.3 起，项目新增了 Supabase Auth 相关依赖：

- `@supabase/supabase-js`
- `@react-native-async-storage/async-storage`
- `react-native-url-polyfill`

检查依赖树：

```bash
npm ls --depth=0
```

---

## 3. 环境变量

本地开发前可以从 `.env.example` 复制出 `.env`：

```bash
cp .env.example .env
```

默认 mock 模式：

```bash
EXPO_PUBLIC_API_MODE=mock
EXPO_PUBLIC_SUPABASE_URL=
EXPO_PUBLIC_SUPABASE_ANON_KEY=
EXPO_PUBLIC_APP_NAME=独家童话
```

真实 Supabase 模式：

```bash
EXPO_PUBLIC_API_MODE=real
EXPO_PUBLIC_SUPABASE_URL=你的 Supabase Project URL
EXPO_PUBLIC_SUPABASE_ANON_KEY=你的 Supabase anon public key
EXPO_PUBLIC_APP_NAME=独家童话
```

注意：

- `.env` 和 `.env.local` 已在 `.gitignore` 中忽略。
- 不要把真实 Supabase URL、anon key 或任何服务端密钥提交到仓库。
- `anon key` 是客户端公开 key，但仍不要写入仓库。
- Supabase service role key 绝对不能放在前端或 `.env.example`。

---

## 4. Supabase 初始化顺序

real 模式使用前，先在 Supabase SQL Editor 中按顺序执行：

```text
1. supabase/schema.sql
2. supabase/rls-policies.sql
```

执行后检查：

- `profiles`、`couples`、`diaries`、`photos`、`anniversaries`、`ai_jobs`、`comments`、`notifications` 八张表存在。
- 八张表都已开启 RLS。
- `public.is_active_couple_member(uuid)` 存在。
- `public.bind_couple_by_invite(text)` 存在。

Auth 登录测试：

1. 在 `.env` 中设置 `EXPO_PUBLIC_API_MODE=real`。
2. 填入 Supabase URL 和 anon key。
3. 在 Supabase Auth 中确认 Email provider 可用。
4. 启动 App。
5. 打开 `/login`。
6. 使用邮箱注册或登录。

---

## 5. 启动命令

常用命令：

```bash
npm run start
npm run android
npm run ios
npm run web
```

指定端口启动：

```bash
npm run start -- --port 8099
```

启动成功后，终端会显示：

- Expo Go 二维码
- Metro 地址，例如 `exp://...`
- Web 地址，例如 `http://localhost:8099`

停止服务：

```text
Ctrl+C
```

---

## 6. Expo 调试方式

### Expo Go 真机

1. 手机安装 Expo Go。
2. 手机和电脑连接同一个局域网。
3. 执行 `npm run start`。
4. 使用 Expo Go 扫描终端二维码。

### Web 调试

执行：

```bash
npm run web
```

或启动后在终端中按 `w`。

### 清理缓存

如果页面热更新异常、路由缓存异常或 Metro 状态混乱，可以执行：

```bash
npm run start -- --clear
```

---

## 7. 常见报错处理

### nvm-desktop: The default Node version is not set

原因：当前终端没有可用的 nvmd 默认 Node 版本。

处理：

```bash
nvmd use 24.3.0
node -v
npm -v
```

如果仍失败，重新打开终端。

### EPERM: operation not permitted, open `.expo/dev/logs/start.log`

原因：Windows 本地 `.expo` 缓存日志权限异常，或目录/文件带压缩属性导致 Expo 无法写日志。

处理：

```powershell
compact /u /s:.expo\dev
```

如仍失败，可删除本地 Expo 缓存后重新启动：

```powershell
Remove-Item -LiteralPath .expo\dev -Recurse -Force
npm run start
```

`.expo/` 是本地生成缓存，已被 `.gitignore` 忽略，不应提交。

### Unable to resolve module

原因通常是 import 路径错误、文件不存在或大小写不一致。

检查顺序：

1. 确认目标文件真实存在。
2. 检查相对路径层级是否正确。
3. 检查文件名大小写。
4. 优先修复 import 路径，不要重复创建同名组件。

### Expo Router route not found

检查：

1. 页面是否放在 `app/` 目录下。
2. 路由跳转路径是否和文件路径一致。
3. 分组目录如 `(tabs)` 不出现在实际 URL 中。
4. `_layout.js` 是否存在且导出了默认布局组件。

### Real API mode is enabled but missing env vars

原因：`.env` 中设置了 `EXPO_PUBLIC_API_MODE=real`，但没有配置 Supabase URL 或 anon key。

处理：

```bash
EXPO_PUBLIC_SUPABASE_URL=你的 Supabase Project URL
EXPO_PUBLIC_SUPABASE_ANON_KEY=你的 Supabase anon public key
```

或者临时切回 mock：

```bash
EXPO_PUBLIC_API_MODE=mock
```

---

## 8. Expo Router 路由规则

项目使用 `expo-router/entry` 作为入口，`app/` 目录即路由目录。

基础规则：

- `app/_layout.js` 是全局 Stack 布局。
- `app/(tabs)/_layout.js` 是底部 Tab 布局。
- `app/(tabs)/index.js` 对应首页 `/`。
- `app/diary/editor.js` 对应 `/diary/editor`。
- `app/photo/upload.js` 对应 `/photo/upload`。

新增页面时：

1. 优先在 `app/` 下按业务模块创建文件。
2. 路由跳转统一使用 `router.push('/path')`。
3. 二级页面建议使用 `FairyBackButton` 或 `FairyHeader showBack` 保持返回行为一致。
4. 不要为了临时跳转创建平行的重复页面。
5. 新增页面后同步更新 `docs/project-file-structure.md`。

---

## 9. 组件新增规则

当前 UI 风格必须保持童话绘本、奶油纸感、桃粉、干玫瑰、可可棕、轻手绘贴纸风格。

新增或修改组件时：

- 优先复用 `src/components/` 中已有组件。
- 页面外壳优先使用 `FairyPage`。
- 页面标题优先使用 `FairyHeader`。
- 卡片优先使用 `FairyCard`。
- 按钮优先使用 `FairyButton`。
- 标签优先使用 `FairyTag`。
- 输入框优先使用 `FairyInput`。
- 空状态优先使用 `FairyEmptyState`。
- 反馈提示优先使用 `FairyToast`。
- 不要引入突兀的默认系统 UI 风格。
- 不要在单次任务中大规模重构所有页面。

新增通用组件后，需要同步更新：

- `docs/project-file-structure.md`
- 必要时更新 `docs/design-system-v1.md`

---

## 10. API 和后端边界

项目支持 mock / real 两种 API 模式。

开发规则：

- 页面不要直接写 Supabase 查询。
- 页面不要直接访问真实后端。
- 真实请求统一放入 `src/api/`。
- Supabase client 只能通过 `src/api/client.js` 创建。
- Auth 相关能力统一通过 `src/api/authApi.js`。
- AI 服务密钥不得出现在前端代码和 `.env.example` 中。
- `.env.example` 只允许写占位变量，不允许写真实密钥。

---

## 11. 提交前检查清单

提交前至少检查：

- `npm install` 无依赖冲突。
- `npm run start` 可以启动 Metro。
- `app/_layout.js` 和相关 `_layout.js` 无明显路由错误。
- 新增 import 路径指向真实文件。
- `.env`、`.env.local`、`.expo/`、`node_modules/` 没有被提交。
- 未写入真实后端密钥或 AI 密钥。
- 新增页面、组件、API、Supabase 文件或文档时，对应项目文档已更新。

---

## 12. 当前推荐开发顺序

1. Phase 5.3：验证 Supabase client 和 Auth 登录。
2. Phase 6.1：日记真实 CRUD。
3. Phase 6.2：照片真实上传与 Storage policy。
4. Phase 6.3：情侣绑定真实流程。
5. Phase 7：AI 任务和 Edge Functions。

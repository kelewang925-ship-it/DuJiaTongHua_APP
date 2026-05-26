# 《独家童话》开发运行手册

> 更新时间：2026-05-26
> 适用范围：Expo React Native / Expo Router 前端开发阶段

本文档用于帮助新开发者拉取项目后完成安装、启动、调试和基础问题排查。当前阶段只运行前端 mock 流程，不接入真实后端。

---

## 1. 环境要求

推荐环境：

- Node.js：24.3.0
- npm：随 Node 24.3.0 安装的 npm 版本
- Expo CLI：使用项目本地依赖，不需要全局安装
- Git
- Expo Go：用于真机扫码调试

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

依赖版本已经在 `package.json` 和 `package-lock.json` 中固定，避免 `latest` 漂移导致 Expo / React Native 版本不一致。

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

当前阶段默认使用：

```bash
EXPO_PUBLIC_API_MODE=mock
```

注意：

- `.env` 和 `.env.local` 已在 `.gitignore` 中忽略。
- 不要把真实 Supabase URL、anon key 或任何服务端密钥提交到仓库。
- 当前阶段不要接入真实后端，只保留占位变量。

---

## 4. 启动命令

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

## 5. Expo 调试方式

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

## 6. 常见报错处理

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

---

## 7. Expo Router 路由规则

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
3. 二级页面建议使用 `FairyBackButton` 保持返回行为一致。
4. 不要为了临时跳转创建平行的重复页面。
5. 新增页面后同步更新 `docs/project-file-structure.md`。

---

## 8. 组件新增规则

当前 UI 风格必须保持童话绘本、奶油纸感、桃粉、干玫瑰、可可棕、轻手绘贴纸风格。

新增或修改组件时：

- 优先复用 `src/components/` 中已有组件。
- 卡片优先使用 `FairyCard`。
- 按钮优先使用 `FairyButton`。
- 标签优先使用 `FairyTag`。
- 输入框优先使用 `FairyInput`。
- 空状态优先使用 `FairyEmptyState`。
- 不要引入突兀的默认系统 UI 风格。
- 不要在单次任务中大规模重构所有页面。

新增通用组件后，需要同步更新：

- `docs/project-file-structure.md`
- 必要时更新 `docs/design-system-v1.md`

---

## 9. API 和后端边界

当前阶段默认 mock 模式。

开发规则：

- 页面不要直接写 Supabase 查询。
- 页面不要直接访问真实后端。
- 后续真实请求统一放入 `src/api/`。
- AI 服务密钥不得出现在前端代码和 `.env.example` 中。
- `.env.example` 只允许写占位变量，不允许写真实密钥。

---

## 10. 提交前检查清单

提交前至少检查：

- `npm install` 无依赖冲突。
- `npm run start` 可以启动 Metro。
- `app/_layout.js` 和相关 `_layout.js` 无明显路由错误。
- 新增 import 路径指向真实文件。
- `.env`、`.env.local`、`.expo/`、`node_modules/` 没有被提交。
- 未写入真实后端密钥或 AI 密钥。
- 新增页面、组件、API 或文档时，对应项目文档已更新。

---

## 11. 当前推荐开发顺序

1. Phase 1.4：新增手动验收清单。
2. Phase 2：补齐前端 MVP 页面闭环。
3. Phase 3：完善组件系统。
4. Phase 4：建立 API mock/real 模式。
5. Phase 5 以后再接入 Supabase。

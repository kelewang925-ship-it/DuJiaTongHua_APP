# Supabase Auth 接入记录

> 文档说明：本文档用于记录《独家童话》Supabase Auth 接入阶段的完成内容、依赖、环境变量、Auth API 封装、登录页改造、控制台设置、验证步骤、已知限制和下一步建议。
> 阶段：Phase 5.3  
> 状态：已接入 Supabase client 与 Auth API 骨架  
> 更新时间：2026-05-26

---

## 1. 本阶段完成内容

Phase 5.3 已完成以下内容：

1. 新增 Supabase Auth 相关依赖。
2. 完善 `src/api/client.js`，支持创建 Supabase client。
3. 新增 `src/api/authApi.js`，封装登录、注册、OTP、退出、session 获取和 profile upsert。
4. 改造 `app/login.js`，从纯展示页变为可交互登录页。
5. 更新 `docs/dev-runbook.md`，补充 Supabase 初始化、环境变量和真实登录测试步骤。

---

## 2. 新增依赖

`package.json` 新增：

```json
{
  "@supabase/supabase-js": "^2.49.8",
  "@react-native-async-storage/async-storage": "^2.2.0",
  "react-native-url-polyfill": "^2.0.0"
}
```

用途：

- `@supabase/supabase-js`：Supabase Auth、Database、Storage 客户端。
- `@react-native-async-storage/async-storage`：React Native 持久化 Supabase session。
- `react-native-url-polyfill`：补齐 React Native 环境中 Supabase client 需要的 URL 能力。

安装后需要执行：

```bash
npm install
```

---

## 3. 环境变量

`.env.example` 当前保留占位变量：

```bash
EXPO_PUBLIC_API_MODE=mock
EXPO_PUBLIC_SUPABASE_URL=
EXPO_PUBLIC_SUPABASE_ANON_KEY=
EXPO_PUBLIC_APP_NAME=独家童话
```

mock 模式：

```bash
EXPO_PUBLIC_API_MODE=mock
```

real 模式：

```bash
EXPO_PUBLIC_API_MODE=real
EXPO_PUBLIC_SUPABASE_URL=你的 Supabase Project URL
EXPO_PUBLIC_SUPABASE_ANON_KEY=你的 Supabase anon public key
```

注意：

- 不要提交 `.env`。
- 不要把真实 key 写入 `.env.example`。
- `service_role` key 不能放在前端。

---

## 4. `src/api/client.js`

当前职责：

- 管理 `mock / real` 模式。
- 提供统一 API 响应结构。
- 提供统一错误归一化。
- 创建 Supabase client 单例。
- 使用 AsyncStorage 持久化 session。

核心函数：

- `getApiMode()`
- `isMockMode()`
- `requestMock(data, ms, meta)`
- `createApiResponse(data, meta)`
- `createApiError(error, fallbackMessage)`
- `normalizeError(error, fallbackMessage)`
- `assertRealModeReady()`
- `getSupabaseConfig()`
- `createSupabaseClient()`
- `getSupabaseClient()`

真实模式下，如果缺少以下变量会抛出错误：

- `EXPO_PUBLIC_SUPABASE_URL`
- `EXPO_PUBLIC_SUPABASE_ANON_KEY`

---

## 5. `src/api/authApi.js`

当前封装函数：

| 函数 | 作用 |
| --- | --- |
| `getCurrentSession()` | 获取当前登录 session。 |
| `signInWithEmailPassword(email, password)` | 邮箱密码登录。 |
| `signUpWithEmailPassword(email, password, profile)` | 邮箱密码注册。 |
| `signInWithOtp(email)` | 发送邮箱登录链接。 |
| `signOut()` | 退出登录。 |
| `upsertProfile(profile)` | 登录后写入或更新 `profiles` 表。 |

mock 模式下，这些函数会返回模拟用户数据，不依赖 Supabase。

real 模式下，这些函数会调用 Supabase Auth 和 `profiles` 表。

---

## 6. 登录页改造

`app/login.js` 当前已从纯展示页改为真实交互页。

支持：

- 邮箱登录
- 注册账号
- 发送邮箱登录链接
- mock/real 模式标签展示
- 登录成功后跳转 `/(tabs)`
- 使用 `FairyInput`、`FairyButton`、`FairyHeader`、`FairyPage`、`FairyToast`

mock 模式默认值：

```text
test@example.com
12345678
```

---

## 7. Supabase 控制台设置

real 模式测试前，需要在 Supabase 控制台确认：

1. 已创建 Supabase 项目。
2. 已执行：

```text
supabase/schema.sql
supabase/rls-policies.sql
```

3. Auth Email provider 可用。
4. 如果使用邮箱登录链接，需要配置 Site URL / Redirect URLs。
5. 如果只测试邮箱密码登录，先确保 Email signup 可用。

---

## 8. 验证步骤

### mock 模式验证

1. `.env` 设置：

```bash
EXPO_PUBLIC_API_MODE=mock
```

2. 执行：

```bash
npm install
npm run start
```

3. 打开 `/login`。
4. 使用默认邮箱和密码点击“进入独家童话”。
5. 应跳转到首页。

### real 模式验证

1. `.env` 设置：

```bash
EXPO_PUBLIC_API_MODE=real
EXPO_PUBLIC_SUPABASE_URL=你的 Supabase Project URL
EXPO_PUBLIC_SUPABASE_ANON_KEY=你的 Supabase anon public key
```

2. 确认已执行数据库结构和 RLS。
3. 启动项目。
4. 打开 `/login`。
5. 注册账号。
6. 检查 Supabase Auth Users 是否出现该用户。
7. 检查 `profiles` 表是否写入 profile。
8. 退出后再次用邮箱密码登录。

---

## 9. 已知限制

当前 Phase 5.3 只完成 Auth 接入骨架和登录页。

尚未完成：

- 启动时自动根据 session 判断跳转。
- 退出登录按钮接入。
- 登录后真实 couple 状态检查。
- 未绑定情侣时跳转邀请页。
- 已绑定情侣时进入首页。
- Storage bucket 和 `storage.objects` policies。
- diary/photo/anniversary 的真实 Supabase CRUD。

---

## 10. 下一步建议

推荐下一步进入：

```text
Phase 6.1：日记真实 CRUD
```

但在开始核心业务真实化前，建议先补一个小任务：

```text
Phase 5.4：登录态启动检查和退出登录
```

建议内容：

1. App 启动时调用 `getCurrentSession()`。
2. 有 session 进入首页。
3. 无 session 进入登录页，或保持当前开发入口策略。
4. 在我的页面增加退出登录入口。
5. 退出后回到 `/login`。

如果要先做数据业务，则从 `diaryApi` 的 real 模式开始最稳。

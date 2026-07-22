# 第二阶段批次记录：Real 日记列表时间展示

## 修复范围

- 提交：`2948e00`（`fix(diary): format real record timestamps in list`）。
- `app/diary/index.js` 改为复用 `formatDiaryDate(diary)`，与日记详情页使用相同的真实时间格式化规则。
- Real Supabase 行经 mapper 后提供 `createdAt`，但不提供 Mock 演示字段 `date`；此前列表页直接读取 `diary.date`，因此错误显示“日期未提供”。

## 验证

- 先新增回归测试并确认其在旧实现上失败。
- 修复后执行 `npm test -- --runInBand src/__tests__/diaryIndexRoute.static.test.js` 通过。
- 执行 `npm run test:final` 通过：93 个测试套件、303 个测试；页面结构、Real 模式、Real 页面和 API 审计均通过。
- `git diff --check` 通过。

## 待人工复验

- 当前项目未运行，A/B 用户也未登录；本批不将旧浏览器会话视为当前可视验收证据。
- 重启项目并以 Real 模式登录任一已绑定用户后，进入 `/diary`，确认真实日记时间与 `/diary/detail` 一致显示。

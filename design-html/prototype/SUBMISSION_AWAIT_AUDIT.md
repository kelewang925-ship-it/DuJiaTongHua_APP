# 提交回调的异步等待审计

本批用 Acorn AST 扫描全部 prototype JS，记录78个直接 busy 回调，均能定位到函数节点；25个声明 async，10个包含直接 await。完整回调、调用表达式、行号、源码与解析器哈希在 evidence/current/submission-await-audit/inventory.json。静态数量不计为行为测试通过数。

## 直接等待的10个回调

| 位置 | 等待与写入顺序 | 本批处理 |
| --- | --- | --- |
| prototype-account:45、prototype-auth-flow:198 | 先等待 Preferences.login；普通登录同步写会话；两步验证显示原生模态Sheet，原页面字段不可操作 | 保留现有策略；登录与二次验证的条件/来源仍随最终异常矩阵复验 |
| prototype-book:15、prototype-capsule:15、prototype-moment:48、prototype-pet:17、prototype-preferences:142 | 当前业务写入在 UI.back 等待前完成；有保护的编辑任务先 commit | 不添加全局字段禁用，不把导航等待当作提交前的数据等待 |
| prototype-pet-life:12 | save 为成长故事、回应、提醒时间、改名或删除；现有保存函数在首次异步让出前完成写入，随后 commit/关闭 | 保留输入与失败机制；没有新增网络保存 |
| prototype-settings:6 | save(inputs) 的共同昵称/标签/显示/手机/两步/反馈同步写入；注销先同步事务，再返回导航Promise | 本批未改设置行为；共同资料上轮31项上下文和4条兼容链保留原指纹 |
| prototype-workshop:43 | W.album 在 Image.decode 后才生成并写入相册记录 | 真实异步写入；本批复现并修复重复导出覆盖与解码错误文案 |

无直接 await 的68个回调仍可能 return 导航Promise或调用其他函数，不能仅凭语法称为同步。inventory保留每个回调和直接调用供复查。本轮沿调用关系检查了记录/时间/宠物/回忆册仓库的本地同步写入、guard.complete和UI.go；未接真实API，也未提出跨标签原子锁保证。

源码审计缩小了“操作开始后普通文本编辑”的实际适用范围；它不替代78个回调的全部分支执行、未来异步实现或整个114页的最终验收。其他事件处理器及图片自动保存仍按各自合同验证，不能用本清单推断其完整性。

## 复跑

在隔离worktree根目录执行：

```powershell
node design-html/prototype/audit_submission_awaits.cjs D:/projectCode/DuJiaTongHua/DuJiaTongHua_APP/node_modules/acorn/dist/acorn.js
```

解析器仅只读复用原工作区已安装的Acorn；不修改原工作区、不新增产品依赖。可将命令第二参数替换为已安装Acorn的绝对路径；版本及实际文件哈希写入报告。

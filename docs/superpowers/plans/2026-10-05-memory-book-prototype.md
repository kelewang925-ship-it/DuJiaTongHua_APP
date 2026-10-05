# 回忆册交互原型 Implementation Plan

> **For agentic workers:** 使用 superpowers:executing-plans 在当前隔离worktree中逐项执行；用户已授权开始并持续推进本目标。

**Goal:** 将m08的21页连接为本地建册、编排、阅读、补页、管理闭环。

**Architecture:** 复用PrototypeUI/Records/Preferences/Dates/PetLife，使用一个简单册集合。每本册有稳定ID，章节、页面、书签、阅读位置、补页都存于册内；来源只保存类型和ID，显示/导出重新检查共同可见性。

**Tech Stack:** 原生HTML/CSS/JavaScript、localStorage、Python Playwright。

**Spec:** design-html/prototype/README.md、INTERACTION_DESIGN.md、BASELINE_PAGES.md中的m08清单及用户完整交互原型提示词。

## Global Constraints

- 仅当前codex/design-html-rebuild worktree，保留原工作区修改。
- 全部21页可编辑；沿用原稿插画和版式，简单交互，不迁移RN/Expo或接真实服务。
- 复用统一Modal/Sheet/Toast/busy/guard/readImage；确认、失败和取消保持原数据。
- 页面完成标志须通过完整要求审计，不能用部分主流程测试置true。

## Review Focus

- 新用户无册/无素材：没有示例册，明确建册/写日记入口。
- 同名不同册：所有读取/写入/删除/补页携稳定册及页ID。
- 来源变私密或删除：阅读/导出/补页隐藏相关内容，保留用户独立编辑文字。
- 返回或保存失败：本地未保存输入不丢失；书签和阅读状态不污染其他册。
- 上传解码/存储不足：有错误及重试，不保存假的photo:true。

## Task 1：首次入口与建册

**Files:** assets/prototype-book-store.js、prototype-book.js、prototype-book.css；custom/pages m08-p01～p05；prototype/verify_book_flow.py。

**Interfaces:** `PrototypeBooks.all()/find(id)/put(book,operation)/remove(id)`；`draft({name,dates,start})`返回status:draft册；键`dujia-prototype-books`。册属性id/name/dates/start/theme/coverPhoto/status/chapters/pages/bookmarks/lastPage/archived/createdAt/updatedAt。

- [ ] 测试：无数据p01→p02；空白建册→主题→p13；完成后p14携id→p15→书架有新册，刷新仍在。
- [ ] 实施：p01真实书架/继续阅读，p02首本CTA，p03当前月份真实共同素材推荐且不擅自生成书，p04字段/日期/dirty保存，p05主题和可见照片选择。
- [ ] 验证：verify_book_flow.py；失败不生成册或跳下一步、取消保留现有册；提交checkpoint。

## Task 2：素材与编排

**Files:** 同上store/controller/css；m08-p06～p14；verify_book_states.py。

**Interfaces:** `sources(book)`返回{kind,id,title,body,image,date,url}；`source(ref,book)`最新可见来源；`savePage(bookId,page)`稳定页ID；`saveStructure(bookId,chapters,pages)`一次提交。

- [ ] 测试：共同日记/照片/时刻/ready工坊/实际宠物故事五来源，过滤私密与草稿；六版式分别到p09/p10/p11/p12或章节编辑，完成后p13包含实际页。
- [ ] 实施：p06真筛选/选择/Empty，p07实际素材预览，p08六版式实际路由；p09摘录/照片/版式替换，p10真图片裁剪/贴纸/文本编辑，p11时刻/照片/说明，p12工坊与宠物实际内容；p13章节CRUD/移动页面/排序，p14真实统计。
- [ ] 验证：缺来源/长正文/保存失败重试/取消/没有模板统一误跳日记页；每种模板写入后能在目录读到；提交checkpoint。

## Task 3：阅读、补页和管理

**Files:** 同上；m08-p15～p21；verify_book_flow.py、verify_book_states.py；assets/prototype-preferences.js。

**Interfaces:** `read(bookId,pageId)/bookmark(bookId,pageId)/supplement(bookId,pageId,data)/rename/archive/remove/exported`；导出及备份包含经过来源检查的册。

- [ ] 测试：目录→指定页→前后页/书签→工具→补页三方式→阅读显示真实补页；两册书签/补页隔离；归档/恢复/改名/删除取消、失败和成功，删除后刷新仍为空。
- [ ] 实施：p15动态目录，p16/p20实际阅读/页码/书签/可滚动长文，p17正确工具Sheet，p18方式选择，p19文字/表情/实际解码图片和未保存保护，p21统一确认删除/安全改名/封面/归档/导出。
- [ ] 验证：源权限变化遮蔽及导出脱敏，真实JSON下载，备份包含册；注销清除册；提交checkpoint。

## Task 4：五宽度及整体验收

**Files:** prototype/verify_book_layout.py、BOOK_IMPLEMENTATION.md、queue.json、README.md、evidence/current。

- [ ] 21页×320/375/390/414/430：长内容、安全区、标题/返回、按钮命中、弹层边界、零脚本错误。
- [ ] 重跑与册来源/备份/首页阅读入口相关的回归；114HTTP文件与custom/pages一致。
- [ ] 记录新行为入口/出口/状态、已修P0/P1/P2及确切未完成项；之后继续114页和共享组件最终审计。

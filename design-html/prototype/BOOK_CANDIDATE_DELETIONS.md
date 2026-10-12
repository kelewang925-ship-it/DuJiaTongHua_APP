# 回忆册章节与书页候选删除结果

5入口×5条件=25项当前执行：保存、返回后继续/放弃、演示保存失败后重试、真实空间不足后重试、另一处更新后拒绝旧编排并放弃。确认删除只改变当前候选，保存排列后才持久化。

种子为3页/2章节，每页已有补页、全页书签、最后阅读page-second、selected素材引用，以及另一册。核对删除章节连同其页、书页及补页消失、书签/最后阅读/selected正确清理、其他页补页和另一册保留、原始来源存储不变。保存检查包含两次快速DOM激活及Loading/禁用；未声称所有输入设备时序已覆盖。

外部更新测试仅另一处修改册名与updatedAt；当前编排保持、拒绝覆盖新数据，放弃后新数据保持。不是全部来源/权限/删除竞争条件。环境390×844减少动效；全114页最终验收仍0。

| 页面／观察索引 | 删除候选 | 保存后剩余章节 | 保存后剩余书页 | 书签／最后阅读 | 当前项数 |
| --- | --- | --- | --- | --- | ---: |
| m08-p13 / 123 | chapter / chapter-state | chapter-two | page-third | page-third / page-third | 5 |
| m08-p13 / 126 | chapter / chapter-two | chapter-state | page-state, page-second | page-state, page-second / page-second | 5 |
| m08-p13 / 124 | page / page-state | chapter-state, chapter-two | page-second, page-third | page-second, page-third / page-second | 5 |
| m08-p13 / 125 | page / page-second | chapter-state, chapter-two | page-state, page-third | page-state, page-third / page-state | 5 |
| m08-p13 / 127 | page / page-third | chapter-state, chapter-two | page-state, page-second | page-state, page-second / page-second | 5 |

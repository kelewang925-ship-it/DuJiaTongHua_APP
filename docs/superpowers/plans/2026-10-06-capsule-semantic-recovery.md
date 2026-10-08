# 胶囊日期与收录关联恢复 Implementation Plan

> 执行方式：使用superpowers:executing-plans逐项实施；在已有独立worktree执行。

**Goal:** 封存胶囊异常日期可明确修正，收录不跳往无关时刻，不提前展示封存内容；恢复CTA不重复。

**Architecture:** 复用PrototypeDates、Capsules本地存储、Preferences.transaction、共享Sheet／Field／Button／Error／protectSheet。日期仅修改opening与updatedAt，保持sealed；原文变化或保存失败保留输入。收录重新读取当前opened胶囊，核对capsuleId，稳定ID碰撞时保留原条目；新时刻继承private。无需新增HTML页或接口。

**Tech Stack:** 既有HTML/CSS/简单JS、本地Storage、隔离Playwright。

**Spec:** design-html/prototype/ISSUES.md I-03/I-04/I-05/I-06及当前完整114页目标。

## 文件与约束

- prototype-capsule-store.js：日期提交与收录身份／幂等／原子写入。
- prototype-capsule.js/css：异常日期共享Error和受保护日期Sheet，保存Loading、失败保持、有效日期正常入口保持。
- prototype-ui.js：内联集合恢复存在时隐藏同集合页后恢复CTA；其他损坏集合入口仍可达。
- 新专项脚本／证据、声明回归检查点与实施记录。所有源码先冻结再验证，旧报告保留自身来源。
- 保持原用户工作区、114页数量、已有视觉语言；不接真实服务，不迁移RN。

## 步骤

- [x] 先复现异常日期无入口、错关联／ID碰撞跳无关时刻、private收录共享与重复恢复CTA。
- [x] 实施日期原文竞争检查、明确保存和dirty保护；日期有效前不提供开启。
- [x] 开启与提醒提交重新读取当前日期／正文／状态，已开启不二次写入；五条额外实际失败基线先验证再修复。
- [x] 收录读当前opened状态，匹配实际capsuleId，碰撞保留原时刻，新时刻继承private并使用既有事务。
- [x] 内联恢复去重，验证Esc／Enter焦点、多集合与外部恢复。
- [x] 冻结源码；专项、时间控件／流程、恢复与备份及连续流程回归；HTTP／全页观察核对；记录仍开放项并提交。

## 继续验收

全部日期字段、失效引用、关系变化、跨窗口编辑、所有页面状态和访问性仍未全产品终验；本阶段不等于目标完成。

Ruling: 日期与收录首轮32条通过后，额外五条证明加载快照会提前开启未来／异常日期并覆盖peer正文；扩展同一Capsules存储提交门以核对当前状态，仍不重构其他模块。

Ruling: 已复现日期保存延迟期间关闭确认仍写入及输入可变，三条基线均失败；关闭取消本次提交，保存锁定输入，继续编辑后重新明确保存。新增三项后最终声明341项，旧338项保留自身源码来源。

验证结果：最终341项检查点通过，源码／报告SHA／HTTP一致；228次观察0错误与0未绑定候选。完整产品目标未完成，继续开放范围。

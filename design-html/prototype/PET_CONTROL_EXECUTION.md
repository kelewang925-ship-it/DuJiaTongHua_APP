# 宠物模块控件执行

## 范围与结果

2026-10-06执行：m07-p01至p25的声明条件下，151个可用初始控件逐项操作。隐藏交互10项、五宽度布局15项、既有流程26项，共202项通过。114页与37共享资产HTTP字节一致；custom/pages一致。只操作隔离测试context。

## 测试条件

已登录、共同关系已绑定；小满与阿舟，固定日期2026-10-06。默认团团为已领养小狗，精力82/饱食76/心情70/亲密160，食物12/5/1、金币50/星星30、已拥有小花围巾及一页成长故事。按页设置领养待确认、未领养、互动结果、低精力、食物不足、奖励结果、缺少星星/金币、整理结果、关联来源删除等条件；详情使用明确稳定ID。完整seed函数见verify_pet_controls.py，未把重定向目标当请求页面验收。

## 修复及诊断

失效成长故事页原返回文字写宠物空间，实际出口为成长时间线。修复顶部可见文字、可访问名称和主按钮文案，出口保持m07-p18。失败基线见baseline/pet-control-hidden-results.json。

首次成就测试在按钮Loading禁用时读取奖励，观察时机错误；等待成功Toast后核对领取状态、库存及防重复。原观察结果保存在baseline/pet-controls-achievement-observer-diagnostic.json。布局第一次对返回按钮统一要求44px，第二次对320px主返回按钮要求44px；实际40px/40.640625px符合用户提示词40~44px。两轮诊断保留，最终对此页返回按钮要求至少40px；其余确认弹层仍要求44px。未修改原设计尺寸，也未将观察阈值问题称为产品修复。

## 隐藏及布局检查

10项：失效页两返回名称/出口；领养输入、装扮预览、小屋布置浏览器返回的继续/放弃；回应取消/Escape/历史返回/拖拽关闭保护；互动及喂食存储配额失败保持整个库存/日志不变，重试只写一次。26项回归涵盖领养、照顾、资源/每日任务、装扮与小屋保存、故事及私密来源、成就奖励、设置及删除失败恢复等。详细有名用例见四份报告。

回复确认、装扮确认、失效故事三个场景各在320/360/390/414/430px测试，共15项。检查屏内边界、按钮热区及继续保留输入/预览，未写入。人工查看320px回复确认及失效故事截图。实际软键盘及所有页面视觉、状态、动效仍需最终综合检查。

## 初始控件契约

| 页面 | 控件 | 实际契约 |
| --- | --- | --- |
| m07-p01 | 提醒 TA 看看 › | remind |
| m07-p01 | 暂时返回 | route:m03-p02 |
| m07-p01 | 返回 | route:m03-p02 |
| m07-p01 | 首页 | route:m03-p02 |
| m07-p01 | 重要时刻 | route:m04-p01 |
| m07-p01 | 工坊 | route:m05-p01 |
| m07-p01 | 宠物 | route:self |
| m07-p01 | 我的 | route:m06-p01 |
| m07-p02 | 小狗 | pressed |
| m07-p02 | 小猫 | pressed |
| m07-p02 | 小兔 | pressed |
| m07-p02 | 小狐狸 | pressed |
| m07-p02 | pet-name | input |
| m07-p02 | 邀请 TA 一起领养 | adopt |
| m07-p02 | 返回 | route:m07-p04 |
| m07-p03 | 互动 | route:m07-p06 |
| m07-p03 | 喂食 | route:m07-p08 |
| m07-p03 | 任务 | route:m07-p11 |
| m07-p03 | 装扮 | route:m07-p12 |
| m07-p03 | 布置小屋 | route:m07-p15 |
| m07-p03 | 成长故事 | route:m07-p18 |
| m07-p03 | 成就图鉴 | route:m07-p21 |
| m07-p03 | 去任务 › | route:m07-p11 |
| m07-p03 | 返回 | route:m03-p02 |
| m07-p03 | 宠物设置 | route:m07-p25 |
| m07-p03 | 首页 | route:m03-p02 |
| m07-p03 | 重要时刻 | route:m04-p01 |
| m07-p03 | 工坊 | route:m05-p01 |
| m07-p03 | 宠物 | route:self |
| m07-p03 | 我的 | route:m06-p01 |
| m07-p04 | 照顾指南 | modal:一起照顾小伙伴 |
| m07-p04 | 宠物日记 | modal:从第一天开始记录 |
| m07-p04 | 一起领养 | route:m07-p02 |
| m07-p04 | 先看看照顾指南 | modal:一起照顾小伙伴 |
| m07-p04 | 返回 | route:m03-p02 |
| m07-p04 | 首页 | route:m03-p02 |
| m07-p04 | 重要时刻 | route:m04-p01 |
| m07-p04 | 工坊 | route:m05-p01 |
| m07-p04 | 宠物 | route:self |
| m07-p04 | 我的 | route:m06-p01 |
| m07-p05 | 再玩一次 | route:m07-p06 |
| m07-p05 | 回到小屋 | route:m07-p03 |
| m07-p05 | 返回 | route:m07-p03 |
| m07-p06 | 摸摸头 / 精力 -5 · 亲密 +3 · 心情 +2 | pressed |
| m07-p06 | 丢球球 / 精力 -12 · 亲密 +3 · 心情 +8 | pressed |
| m07-p06 | 讲故事 / 精力 -8 · 亲密 +6 · 心情 +4 | pressed |
| m07-p06 | 送小礼物 / 礼物 1 份 · 消耗1份 | pressed |
| m07-p06 | 和团团互动 | play |
| m07-p06 | 返回 | route:m07-p03 |
| m07-p07 | 宠物空间 | route:m07-p03 |
| m07-p07 | 成长日记 | route:m07-p18 |
| m07-p07 | 去喂食补充精力 › | route:m07-p08 |
| m07-p08 | 香香主粮 / ×12 / 饱食+12 精力+15 | pressed |
| m07-p08 | 爱心小饼干 / ×5 / 饱食+8 精力+8 心情+2 | pressed |
| m07-p08 | 草莓布丁 / ×1 / 饱食+20 精力+20 心情+5 | pressed |
| m07-p08 | 喂给团团 | feed |
| m07-p08 | 去获得更多食物 › | route:m07-p11 |
| m07-p08 | 返回 | route:m07-p03 |
| m07-p09 | 返回 | route:m07-p03 |
| m07-p09 | 去做任务 | route:m07-p11 |
| m07-p10 | 返回任务 | route:m07-p11 |
| m07-p10 | 返回 | route:m07-p03 |
| m07-p11 | 每日任务 | tab |
| m07-p11 | 本周约定 | tab |
| m07-p11 | 返回小屋 | route:m07-p03 |
| m07-p11 | 返回 | route:m07-p03 |
| m07-p11 | 给宠物添水 | water |
| m07-p11 | 陪宠物互动 | route:m07-p06 |
| m07-p11 | 给宠物喂食 | route:m07-p08 |
| m07-p11 | 整理宠物小屋 | route:m07-p15 |
| m07-p11 | 记录今天的小心情 | sheet:宠物小心情 |
| m07-p12 | 返回宠物小屋 | route:m07-p03 |
| m07-p12 | 衣服 | tab |
| m07-p12 | 配饰 | tab |
| m07-p12 | 小物 | tab |
| m07-p12 | 不佩戴 | none |
| m07-p12 | 小花围巾 已拥有 | catalog:scarf |
| m07-p12 | 格纹蝴蝶结 金币20 | catalog:bow |
| m07-p12 | 星星领结 亲密度160 | catalog:star-bow |
| m07-p12 | 蜜桃帽子 记录一页成长故事 | catalog:peach-hat |
| m07-p12 | 星光皇冠 星星30 | catalog:crown |
| m07-p12 | 保存这身搭配 | outfit-save |
| m07-p13 | 宠物空间 | route:m07-p03 |
| m07-p13 | 去做任务 | route:m07-p11 |
| m07-p14 | 继续布置 | route:m07-p15 |
| m07-p14 | 回到小屋 | route:m07-p03 |
| m07-p14 | 返回 | route:m07-p03 |
| m07-p15 | 地毯 | tab |
| m07-p15 | 小床 | tab |
| m07-p15 | 墙饰 | tab |
| m07-p15 | 摆件 | tab |
| m07-p15 | 花朵地毯 已拥有 | catalog:flower-rug |
| m07-p15 | 格纹地毯 金币20 | catalog:plaid-rug |
| m07-p15 | 月亮地毯 亲密度160 | catalog:moon-rug |
| m07-p15 | 野餐垫 照顾7个不同日期 | catalog:picnic-rug |
| m07-p15 | 保存小屋布置 | room-save |
| m07-p15 | 返回 | route:m07-p03 |
| m07-p16 | 返回 | route:m07-p03 |
| m07-p16 | 去做任务 | route:m07-p11 |
| m07-p17 | 返回成长时间线 | route:m07-p18 |
| m07-p17 | 返回成长时间线 | route:m07-p18 |
| m07-p18 | 写一页成长故事 | sheet:成长故事 |
| m07-p18 | 返回 | route:m07-p03 |
| m07-p18 | 2026-10-05 · 小满 / 共同成长故事 | route:m07-p19:id=pet-story |
| m07-p18 | 关联共同记录 | sheet:关联共同记录 |
| m07-p19 | 写下今天的下一页 | sheet:成长故事 |
| m07-p19 | 返回 | route:m07-p18 |
| m07-p19 | 回应这一页 | sheet:回应 |
| m07-p20 | 返回 | route:m07-p03 |
| m07-p20 | 领取奖励 | achievement |
| m07-p21 | 第一次见面 可领取奖励 | route:m07-p20:achievement=meet |
| m07-p21 | 玩到天黑 0 / 10 | route:m07-p20:achievement=play10 |
| m07-p21 | 默契喂食 0 / 20 | route:m07-p20:achievement=feed20 |
| m07-p21 | 小屋变新了 0 / 1 | route:m07-p20:achievement=room |
| m07-p21 | 照顾7天 1 / 7 | route:m07-p20:achievement=care7 |
| m07-p21 | 亲密搭档 可领取奖励 | route:m07-p20:achievement=affinity |
| m07-p21 | 陪伴30天 可领取奖励 | route:m07-p20:achievement=days30 |
| m07-p21 | 去完成今天的照顾 | route:m07-p11 |
| m07-p21 | 返回 | route:m07-p03 |
| m07-p21 | 收藏图鉴 | route:m07-p22 |
| m07-p22 | 装扮 | tab |
| m07-p22 | 小屋 | tab |
| m07-p22 | 纪念物 | tab |
| m07-p22 | 小花围巾 已拥有 | catalog:scarf |
| m07-p22 | 格纹蝴蝶结 金币20 | catalog:bow |
| m07-p22 | 星星领结 亲密度160 | catalog:star-bow |
| m07-p22 | 蜜桃帽子 记录一页成长故事 | catalog:peach-hat |
| m07-p22 | 星光皇冠 星星30 | catalog:crown |
| m07-p22 | 雨天小斗篷 照顾7个不同日期 | catalog:cape |
| m07-p22 | 暖暖小马甲 金币20 | catalog:vest |
| m07-p22 | 晚安铃铛 喂食20次 | catalog:bell |
| m07-p22 | 返回 | route:m07-p03 |
| m07-p22 | 认识小伙伴 | sheet:四位小伙伴 |
| m07-p23 | 返回图鉴 | route:m07-p22 |
| m07-p23 | 去换上 | equip |
| m07-p23 | 返回图鉴 | route:m07-p22 |
| m07-p24 | 先导出成长记录 | export |
| m07-p24 | 暂时解除共同照顾 | modal:暂停共同照顾？ |
| m07-p24 | 我再想想，返回 | route:m07-p25 |
| m07-p24 | 返回 | route:m07-p25 |
| m07-p25 | 返回宠物空间 | route:m07-p03 |
| m07-p25 | 共同提醒 / 每天 20:30 · 本地提醒 | sheet:提醒时间 |
| m07-p25 | 共同提醒 | setting |
| m07-p25 | 照顾通知 | setting |
| m07-p25 | 照顾通知 | setting |
| m07-p25 | 成长故事自动收录 | setting |
| m07-p25 | 成长故事自动收录 | setting |
| m07-p25 | 导出团团的成长记录 | export |
| m07-p25 | 仅我们可见说明 | modal:仅我们可见 |
| m07-p25 | 暂时解除共同照顾 | route:m07-p24 |
| m07-p25 | 更多 | sheet:宠物资料与数据 |

## 来源及验收边界

当前源码指纹：`14cff83649ae551d556656f2d7294947e338a59070ab5cee40a5a341e2df48b5`。pet-controls-checkpoint.json绑定151/10/15/26项报告与当前源码；旧阶段证据保存在history/pre-pet-controls-7311c3b，文件夹名为归档时HEAD。此前设置116项不累计为本轮当前源码全部通过。

累计93页建立初始控件契约，余下21页回忆册继续；114页最终验收0。动态条件全覆盖、所有组件热区/视觉/安全区/键盘/动效、跨模块连续流程及其他集合恢复仍待完成，目标保持active。

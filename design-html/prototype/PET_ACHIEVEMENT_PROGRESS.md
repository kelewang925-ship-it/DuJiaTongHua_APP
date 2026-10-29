# 宠物成就进度与真实数据对应

P2-VIS-PET-PROGRESS：m07-p20 控制器更新了四行成就名称及分数，底图中的非零进度条、锁及完成印章却仍显示。原实现的0/10、0/20与非零条矛盾；四行实际成就是“第一次见面／玩到天黑／默契喂食／小屋变新了”，不能把原稿睡觉30次或5/12写入真实模型来匹配图片。

## 实现

- 继续使用 `PrototypePetLife.achievements` 的名称、进度、目标、达成及领取状态。计数、目标、奖励和领奖函数完全未改。
- 只为本页载入展示辅助层，在原四行内容区域覆盖旧进度、锁和印章。保留左侧宠物插画、纸卡边框、大幅抱星宠物及页面入口；原全局 `.stamp` 隐藏，避免所选成就的状态错误地印在第一行上。
- 四行使用原生 `progress`、明确的分数和“进行中／已达成／奖励已领取”。视觉值封顶到目标，0值无填充，完成为满格；标签和 `aria-valuetext` 提供同一份状态。进度不是新的按钮，没有增加点击行为。
- 图像复查发现奖励文本与原星星图标重叠，记录实际文字范围后，仅用本页CSS将奖励文本放到图标右侧。奖励金额和领取流程保持。
- 原共享控制器只在既有行文字赋值后调用展示辅助层；移除这次接入即可逐字恢复原控制器。没有新增宠物状态、成就、奖励类型或业务规则。

## 当前验证

当前 **26/26 新执行通过**：

| 范围 | 数量 |
| --- | --- |
| 五宽度320/360/390/414/430 × 零值、部分、完成、超目标／已领；四行标签、分数、原生value/max、领取状态、纸卡边界、旧印章隐藏、奖励文字避开星星、存储不变 | 20 |
| 原返回与领取奖励两个初态入口，原days30奖励仍增加30星星 | 2 |
| play10领奖失败保留／重试加10且只领一次并重载保持；实际玩耍从9到10；实际喂食从19到20；同浏览器另一标签页写入后通过真实storage事件刷新4/10到7/10 | 4 |

四种390宽截图均已实际查看，零值时“第一次见面”1/1满格是正确的已达成状态，其他0值行为空。上方汇总仍按全部七项成就计算，不把四条可见行当成全部成就。

证据：[当前结果](evidence/current/pet-achievement-progress/results.json)、[检查点](evidence/current/pet-achievement-progress/checkpoint.json)、[零值](evidence/current/pet-achievement-progress/zero.png)、[部分](evidence/current/pet-achievement-progress/partial.png)、[已领取及超目标](evidence/current/pet-achievement-progress/over-target.png)。

## 保留的阶段边界

- `evidence/baseline/pet-achievement-progress` 保存原20项失败、旧截图、原HTML／控制器、精确替换和实际生产脚本。
- 第一版26/26只包含进度及业务验证，图像复查才发现奖励文字压图标，原报告、CSS、生产脚本及实际范围相交诊断保存到 `pet-achievement-progress-before-reward-label`，不把该版本当最终视觉正确。
- 当前26项包含新增奖励文字边界断言，全部按最终源重新执行，没有以旧26项冒充新源通过。
- 检查点核实既有三个文件精确反向恢复、镜像、只有p20加载辅助层，原插画、两个宠物store及其他依赖保持。其他宠物页面本批未重新全量执行，旧报告保持源版本。

使用现有Playwright Python环境与8765预览服务复验：

```powershell
python design-html/prototype/verify_pet_achievement_progress_checkpoint.py
```

完整浏览器运行器为 `verify_pet_achievement_progress.py --stage current`，拒绝覆盖已有报告，重跑前先保存原证据和对应源版本。

本批修复已复现的进度误导及本页奖励文本遮图标。宠物头像／气泡避让、库存及预览与静态示例对应、字体等问题继续，114页完整目标及人工验收状态不变，人工仍0。

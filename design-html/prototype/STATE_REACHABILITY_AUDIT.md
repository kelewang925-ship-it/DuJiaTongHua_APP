# 来源页与操作落点的证据核对

本批为证据整理，没有重新执行浏览器，也没有修改产品代码。检查当前8份初始控件报告、原完整复验检查点、实际fixture脚本和后续相册单函数变更范围。

## 核对结果

- 8份报告合计包含114个明确来源页面的已通过控件记录，覆盖原有114页。
- 仅取操作完成后的URL，只有106个不同页面。来源页上的按钮通常会离开该页，因此最终落点集合不是页面可到达清单。
- 原报告、脚本和源码指纹保持；当前源码相对原完整复验仅私有decodedImage不同，其影响范围与117项相册检查另有证明。本批不改旧报告哈希、不冒充当前源码重新执行全部测试。
- 每页来源控件的报告路径、行索引、selector、标签、合同、观察URL（原报告有时才记录）及操作落点已加入既有`queue.json`的`automated_evidence.origin_control`。未建立第二份114页清单。

## 最终落点集合未包含的8页

| 设计状态 | 原报告中实际来源页证明 |
| --- | --- |
| m02-p08 邀请失效 | onboarding-control-results：重新邀请／重新输入；原登录关联流程另含失效进入与重新输入 |
| m02-p09 已有关系冲突 | onboarding-control-results：回到我们的首页／查看关系设置；关系保持流程另有显式断言 |
| m07-p07 精力不足 | pet-controls inventory保留实际cost=5来源URL；补充精力入口和出口控件通过 |
| m07-p09 食物不足 | pet-controls inventory记录本页及“去做任务”；并非只有喂食后落点 |
| m07-p10 领取奖励 | pet-controls inventory记录pet-reward来源ID和返回任务动作 |
| m07-p13 装扮资源不足 | pet-controls inventory记录item=crown来源URL、任务出口；fixture声明星星为0 |
| m07-p17 关联故事不可见 | pet-controls inventory记录pet-blocked来源ID及返回成长时间线动作；fixture声明失效来源 |
| m08-p02 空书架 | book-controls inventory记录本页、“新建第一本回忆册”及到基础编辑的真实操作 |

这8页不是本次发现的缺页；差异来自索引只统计了操作后的URL。存在来源页与已验证出口，不等于该页所有条件、视觉、文案及异常组合已最终通过。

## 可复核入口

`audit_state_reachability.py`校验8份报告的原检查点绑定、fixture脚本指纹、当前源码差异、CSS一致与114份custom／pages镜像字节，更新唯一主清单的证据索引。结果为`evidence/current/state-reachability/checkpoint.json`：来源114、不同最终落点106、浏览器新增执行0、最终验收0。

开发、交互、视觉状态保持原值；人工验收、黄金名单及完整动态条件继续按原目标核对。

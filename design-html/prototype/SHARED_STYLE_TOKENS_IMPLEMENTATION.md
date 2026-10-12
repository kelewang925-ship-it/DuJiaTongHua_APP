# 动态样式共享Token接入

12个prototype CSS中的504处语义声明接入现有Token及16个新增变量。全部值保持相同；CSS控制器、原稿HTML、图片资源、位置/cqw/渐变与独有主题色没有改写。40px控件只命名为compact，不把它算成44px触摸验收。其他独有字号/色值、动态JS样式及原稿局部Token决定仍需审计。

## 新增语义变量

| Token | 保持的值 |
| --- | --- |
| --prototype-font-family | Fairy,serif |
| --prototype-control-compact | 40px |
| --prototype-paper-warm | #fffaf0 |
| --prototype-ink-warm | #66432d |
| --prototype-border-warm | #edd0b8 |
| --prototype-button-primary | #f6bec8 |
| --prototype-button-secondary | #f5eae6 |
| --prototype-tag-paper | #f9e7d3 |
| --prototype-tag-border | #dfb99a |
| --prototype-tag-ink | #583a26 |
| --prototype-loading-base | #ede2dc |
| --prototype-toast-error | #854d48 |
| --prototype-overlay | #4a363680 |
| --prototype-motion-feedback | 120ms |
| --prototype-motion-fade | 160ms |
| --prototype-motion-spin | 900ms |

## 实际证据

31589退出0：12代表界面×五宽度的60份计算样式基线；迁移后98377退出0，60份可见元素的22项计算属性逐份相同。包括留言Avatar、标签页以及各模块。不是114页全部运行与状态验收。

96125退出0：归档CSS与当前CSS分别实际加载，在普通/减少动效模式比较弹窗/标题/聚焦字段/行内错误/禁用按钮/Spinner/遮罩。普通弹窗220ms和Spinner900ms保持，减少动效均0s。该补充是组件样式契约，不能代替业务流程。

独立校验按变化清单恢复原CSS字节，逐声明展开实际变量值比较原值，检查只有这12份CSS发生产品源变化，114份HTML都加载共享样式；151个HTTP文件逐份匹配当前源。原始CSS字节、迁移清单与实际执行报告保留。迁移工具拒绝第二次apply覆盖基线；check当前未迁移的本批候选为0。

## 后续

当前专项证明等值接入，完整114页清单/初始与隐藏动作/主要流程及异常/键盘/安全区/全部视觉继续。此前17组件、字段、752初始动作等证据保留历史属性。局部Token并非全部完成；0页终验，目标继续。

校验脚本最初把独立书册主题变量--book-paper当作全局常量，误报其合法主题差异；随后只展开本批实际使用的--prototype-*公共变量，书册表达式原样保持。生产CSS与60+2执行结果未改变，修正后的独立校验实际退出0。

# 当前共享Token根节点观察

> 局部接入补齐：10份后续动态CSS的191处声明复用18个既有变量；22份动态CSS按既有精确同值政策检查剩余可替换0。修改前151观察、修改后72受影响场景的计算属性／几何／伪元素完全一致，根变量定义未改。下面43项表保留2026-10-31实际观察日期，不冒充重采。见[CURRENT_STYLE_TOKEN_ADOPTION](CURRENT_STYLE_TOKEN_ADOPTION.md)。

2026-10-31，114个canonical页面、390px宽、减少动效下实际读取43项共享变量。核心颜色、字体、间距、圆角、阴影和控件尺寸在114页均非空且值一致。根变量一致不证明局部CSS已完全采用变量，也不等于像素或人工验收。

| Token | 实际不同值 | 非空页数 |
| --- | --- | ---: |
| --prototype-accent | #b08a8f | 114/114 |
| --prototype-border | #d4bdb6 | 114/114 |
| --prototype-border-warm | #edd0b8 | 114/114 |
| --prototype-button-primary | #f6bec8 | 114/114 |
| --prototype-button-secondary | #f5eae6 | 114/114 |
| --prototype-control-compact | 40px | 114/114 |
| --prototype-control-height | 48px | 114/114 |
| --prototype-danger | #985b50 | 114/114 |
| --prototype-font-body | 16px | 114/114 |
| --prototype-font-family | Fairy,serif | 114/114 |
| --prototype-font-note | 14px | 114/114 |
| --prototype-font-title | 20px | 114/114 |
| --prototype-gap | 16px | 114/114 |
| --prototype-ink | #6b4f4f | 114/114 |
| --prototype-ink-warm | #66432d | 114/114 |
| --prototype-loading-base | #ede2dc | 114/114 |
| --prototype-motion-enter | 220ms | 114/114 |
| --prototype-motion-fade | 160ms | 114/114 |
| --prototype-motion-feedback | 120ms | 114/114 |
| --prototype-motion-spin | 900ms | 114/114 |
| --prototype-nav-height | 68px | 114/114 |
| --prototype-overlay | #4a363680 | 114/114 |
| --prototype-paper | #fdfbf7 | 114/114 |
| --prototype-paper-warm | #fffaf0 | 114/114 |
| --prototype-radius | 20px | 114/114 |
| --prototype-radius-md | 12px | 114/114 |
| --prototype-radius-sm | 8px | 114/114 |
| --prototype-shadow | 0 12px 32px #6b4f4f29 | 114/114 |
| --prototype-space-lg | 16px | 114/114 |
| --prototype-space-md | 12px | 114/114 |
| --prototype-space-sm | 8px | 114/114 |
| --prototype-space-xl | 24px | 114/114 |
| --prototype-space-xs | 4px | 114/114 |
| --prototype-space-xxl | 32px | 114/114 |
| --prototype-tag-border | #dfb99a | 114/114 |
| --prototype-tag-ink | #583a26 | 114/114 |
| --prototype-tag-paper | #f9e7d3 | 114/114 |
| --prototype-toast-error | #854d48 | 114/114 |
| --prototype-touch | 44px | 114/114 |
| --ui-focus | #a45f63 | 114/114 |
| --ui-focus-soft | #dca2a7 | 114/114 |
| --ui-safe-bottom | 0px | 114/114 |
| --ui-safe-top | 0px | 114/114 |

## 来源与剩余

[实际报告](evidence/current/components-20261031/results.json)逐页存有原始值与源码／样式指纹。旧228次观察及504处等值迁移说明已[归档](evidence/history/pre-current-components-af7c4b1/TOKEN_COVERAGE.md)，其历史指纹不改写为新源码。

原画板的绘画、位置和有依据的局部皮肤继续按保留决定核对；不能仅因局部存在颜色字面量就替换成统一值。局部选择器、状态与主题的Token使用及完整41项终审继续，人工验收0。
